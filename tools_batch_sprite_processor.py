import os
import zlib
import struct
import math
import sys

def write_png(filename, width, height, pixels):
    raw_data = bytearray()
    for row in pixels:
        raw_data.append(0) # Filter 0 (None)
        for r, g, b, a in row:
            raw_data.extend([int(r)&0xFF, int(g)&0xFF, int(b)&0xFF, int(a)&0xFF])
            
    compressed = zlib.compress(bytes(raw_data), level=9)
    png = bytearray(b'\x89PNG\r\n\x1a\n')
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    png.extend(struct.pack('>I', len(ihdr)) + b'IHDR' + ihdr + struct.pack('>I', zlib.crc32(b'IHDR' + ihdr)))
    png.extend(struct.pack('>I', len(compressed)) + b'IDAT' + compressed + struct.pack('>I', zlib.crc32(b'IDAT' + compressed)))
    png.extend(struct.pack('>I', 0) + b'IEND' + struct.pack('>I', zlib.crc32(b'IEND')))
    
    with open(filename, 'wb') as f:
        f.write(png)

def read_png(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    if data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError(f"{filename} 不是標準 PNG 格式！")
    
    pos = 8
    width = height = bit_depth = color_type = None
    idat_chunks = []
    
    while pos < len(data):
        length = struct.unpack('>I', data[pos:pos+4])[0]
        ctype = data[pos+4:pos+8]
        cdata = data[pos+8:pos+8+length]
        pos += 8 + length + 4
        
        if ctype == b'IHDR':
            width, height, bit_depth, color_type = struct.unpack('>IIBB', cdata[:10])
        elif ctype == b'IDAT':
            idat_chunks.append(cdata)
        elif ctype == b'IEND':
            break
            
    decompressed = zlib.decompress(b''.join(idat_chunks))
    bytes_per_pixel = 4 if color_type == 6 else 3
    stride = width * bytes_per_pixel + 1
    
    pixels = []
    prev_row = [0] * (width * bytes_per_pixel)
    
    for y in range(height):
        row_data = decompressed[y*stride : (y+1)*stride]
        filter_type = row_data[0]
        curr_row = list(row_data[1:])
        
        if filter_type == 1:
            for i in range(bytes_per_pixel, len(curr_row)):
                curr_row[i] = (curr_row[i] + curr_row[i - bytes_per_pixel]) & 0xFF
        elif filter_type == 2:
            for i in range(len(curr_row)):
                curr_row[i] = (curr_row[i] + prev_row[i]) & 0xFF
        elif filter_type == 3:
            for i in range(len(curr_row)):
                a = curr_row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
                b = prev_row[i]
                curr_row[i] = (curr_row[i] + ((a + b) >> 1)) & 0xFF
        elif filter_type == 4:
            for i in range(len(curr_row)):
                a = curr_row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
                b = prev_row[i]
                c = prev_row[i - bytes_per_pixel] if i >= bytes_per_pixel else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if pa <= pb and pa <= pc else (b if pb <= pc else c)
                curr_row[i] = (curr_row[i] + pr) & 0xFF
                
        prev_row = curr_row[:]
        row_pixels = []
        for x in range(width):
            idx = x * bytes_per_pixel
            if bytes_per_pixel == 4:
                row_pixels.append(curr_row[idx:idx+4])
            else:
                row_pixels.append(curr_row[idx:idx+3] + [255])
        pixels.append(row_pixels)
        
    return width, height, pixels

def auto_remove_background(pixels, bg_color='black', tolerance=30):
    """
    純 Python 批次去除純黑、純白或純綠底色，並進行羽化過渡
    """
    h = len(pixels)
    w = len(pixels[0])
    out = []
    
    for y in range(h):
        row = []
        for x in range(w):
            r, g, b, a = pixels[y][x]
            if bg_color == 'black':
                # 黑色/深色底去除 (針對暗色背景的攻擊特效或怪物)
                lum = max(r, g, b)
                if lum < tolerance:
                    row.append([0, 0, 0, 0])
                elif lum < tolerance + 40:
                    alpha = int((lum - tolerance) / 40.0 * 255)
                    row.append([r, g, b, min(a, alpha)])
                else:
                    row.append([r, g, b, a])
            elif bg_color == 'white':
                # 白色/純亮底去除
                min_c = min(r, g, b)
                if min_c > 255 - tolerance:
                    row.append([0, 0, 0, 0])
                elif min_c > 255 - tolerance - 40:
                    alpha = int((255 - min_c) / 40.0 * 255)
                    row.append([r, g, b, min(a, alpha)])
                else:
                    row.append([r, g, b, a])
            elif bg_color == 'green':
                # 綠幕去除
                if g > 150 and g > r * 1.4 and g > b * 1.4:
                    row.append([0, 0, 0, 0])
                else:
                    row.append([r, g, b, a])
            else:
                row.append([r, g, b, a])
        out.append(row)
    return out

def slice_spritesheet(sheet_path, rows, cols, output_dir, prefix="anim_frame", bg_color=None):
    """
    將一張包含 rows x cols 的怪物動作精靈圖自動切片並去背輸出
    """
    os.makedirs(output_dir, exist_ok=True)
    w, h, pixels = read_png(sheet_path)
    
    frame_w = w // cols
    frame_h = h // rows
    
    print(f"🎬 開始切片: 原始尺寸 {w}x{h} -> 網格 {cols}x{rows}，單幀大小 {frame_w}x{frame_h}")
    
    frame_idx = 1
    rpy_frames = []
    
    for r in range(rows):
        for c in range(cols):
            start_x = c * frame_w
            start_y = r * frame_h
            
            frame_pixels = []
            for y in range(start_y, start_y + frame_h):
                row = []
                for x in range(start_x, start_x + frame_w):
                    row.append(pixels[y][x])
                frame_pixels.append(row)
                
            if bg_color:
                frame_pixels = auto_remove_background(frame_pixels, bg_color)
                
            out_name = f"{prefix}_{frame_idx:02d}.png"
            out_file = os.path.join(output_dir, out_name)
            write_png(out_file, frame_w, frame_h, frame_pixels)
            rpy_frames.append(out_name)
            frame_idx += 1
            
    print(f"✨ 成功切片並儲存 {len(rpy_frames)} 張動畫幀至: {output_dir}")
    
    # 自動產生 Ren'Py ATL 動畫代碼
    anim_name = prefix
    print("\n" + "="*50)
    print("📋 自動產生的 Ren'Py ATL 動畫腳本代碼 (可直接貼入 .rpy):")
    print("="*50)
    print(f"image {anim_name}:")
    for f_name in rpy_frames:
        print(f'    "images/monsters/{f_name}"')
        print(f"    0.10")
    print("    repeat")
    print("="*50 + "\n")

if __name__ == "__main__":
    print("🛠️ 《無限之夜》怪物多幀動畫快速切片與批次去背工具已就緒。")

