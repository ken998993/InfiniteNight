# ==============================================================================
# 🎮 《輪迴世界》即時動作突圍戰場系統 (action_battlefield.rpy)
# 依據 developMd/18_battlefield.md 與最新戰術要求實裝
# 背景：zombieroom.jpg
# 玩家小人：c1.png (支援上下左右四向移動、真實即時射擊、受創無敵閃爍)
# 怪物：agile_zombie.jpg (即時全向追蹤逼近、頭頂動態血條、受擊硬直擊退)
# 特效：浮動傷害數值、暴擊字樣、受擊血花、碰撞震屏、全螢幕受創血霧
# ==============================================================================

init -3 python:
    BATTLE_BLACK_BG = Solid("#000000")
    BATTLE_DOOR_DISP = Solid("#00ffff66")

init -2 python:
    import math
    import random
    import time
    try:
        import pygame_sdl2 as pygame
    except ImportError:
        import pygame

    class ActionZombieBattleDisplayable(renpy.Displayable):
        black_bg = BATTLE_BLACK_BG
        door_disp = BATTLE_DOOR_DISP
        map_w = 3840.0
        map_h = 2160.0
        current_room = 'zombieroom'

        def __init__(self, target_kills=8, **kwargs):
            super(ActionZombieBattleDisplayable, self).__init__(**kwargs)
            self.target_kills = target_kills
            
            # 載入主美術圖檔與精靈 (精確縮放至地圖尺寸 3840x2160)
            self.bg_disp = Transform("images/zombieroom.jpg", xsize=3840, ysize=2160)
            self.black_bg = BATTLE_BLACK_BG
            self.door_disp = BATTLE_DOOR_DISP
            
            self.player_right = Transform("images/c1.png", xsize=80, ysize=115)
            self.player_left = Transform("images/c1.png", xsize=80, ysize=115, xzoom=-1)
            self.zombie_normal = Transform("images/agile_zombie.jpg", xsize=80, ysize=80)
            
            # 特效圖元
            self.red_flash = Solid("#ff2222aa", xsize=80, ysize=80)
            self.screen_hurt_disp = Solid("#ff000055", xsize=1920, ysize=1080)
            self.bullet_disp = Solid("#00ffff", xsize=12, ysize=12)
            self.particle_disp = Solid("#ff3333", xsize=8, ysize=8)
            self.spark_disp = Solid("#ffff33", xsize=6, ysize=6)
            
            # 血條圖元
            self.hp_bar_bg = Solid("#220000", xsize=60, ysize=7)
            self.hp_bar_fg = Solid("#00ff66", xsize=60, ysize=7)
            self.hp_bar_danger = Solid("#ff3333", xsize=60, ysize=7)
            
            # 重置遊戲狀態
            self.reset_game()

        def reset_game(self):
            self.current_room = 'zombieroom'
            self.bg_disp = Transform("images/zombieroom.jpg", xsize=3840, ysize=2160)
            
            # 地圖大小 (等於放大後的背景圖大小)
            self.map_w = 3840.0
            self.map_h = 2160.0
            
            # 四向房間傳送點 (位於放大 1.2 倍後的菱形四個角落內側)
            self.doors = {
                'northwest': {'x': 880.0,  'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'northwest_area', 'spawn_at': 'southeast'},
                'northeast': {'x': 2960.0, 'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'labortary1',     'spawn_at': 'southwest'},
                'southwest': {'x': 880.0,  'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southwest_area', 'spawn_at': 'northeast'},
                'southeast': {'x': 2960.0, 'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southeast_area', 'spawn_at': 'northwest'}
            }
            
            # 玩家數值 (起始在中心)
            self.player_x = self.map_w / 2
            self.player_y = self.map_h / 2
            self.player_speed = 340.0
            self.player_hp = 100
            self.player_max_hp = 100
            self.player_iframes = 0.0      # 受傷無敵時間 (秒)
            self.facing = 1                # 1 朝右, -1 朝左
            self.aim_angle = 0.0           # 射擊角度 (弧度)
            
            # 攝影機座標 (左上角)
            self.cam_x = 0.0
            self.cam_y = 0.0
            
            # 射擊狀態
            self.bullets = []              # [ {x, y, vx, vy, life} ]
            self.last_shot_time = 0.0
            self.shot_cooldown = 0.16      # 射速：每 0.16 秒一發
            self.last_melee_time = 0.0
            self.melee_cooldown = 0.4      # 近戰冷卻時間
            
            # 怪物列表
            self.zombies = []              # [ {id, x, y, hp, max_hp, speed, hurt_timer, is_dead} ]
            self.zombie_id_counter = 0
            self.last_spawn_time = 0.0
            self.spawn_interval = 1.8      # 每 1.8 秒刷新一隻
            self.max_active_zombies = 4
            self.spawned_count = 0
            
            # 視覺特效
            self.floating_texts = []       # [ {text, x, y, vy, life, color, size} ]
            self.particles = []            # [ {x, y, vx, vy, life, color, size} ]
            self.screen_shake = 0.0
            self.screen_hurt_vignette = 0.0
            
            # 戰局進度
            self.kills = 0
            self.state = 'playing'         # 'playing', 'won', 'lost'
            
            # 輸入鍵位
            self.keys_down = set()
            self.mouse_x = 960
            self.mouse_y = 540
            self.last_st = None
            
            # 初始先刷新 2 隻敏捷型喪屍
            self.spawn_zombie()
            self.spawn_zombie()

        def spawn_zombie(self):
            if self.spawned_count >= self.target_kills * 2 and len(self.zombies) >= self.max_active_zombies:
                return
                
            # 在距離玩家半徑 1200 像素的圓周上隨機生成 (確保在 1920x1080 螢幕之外)
            angle = random.uniform(0, math.pi * 2)
            spawn_dist = 1200.0
            sx = self.player_x + math.cos(angle) * spawn_dist
            sy = self.player_y + math.sin(angle) * spawn_dist
            
            # 限制在地圖邊界內
            sx = max(50.0, min(self.map_w - 50.0, sx))
            sy = max(50.0, min(self.map_h - 50.0, sy))
            
            self.zombie_id_counter += 1
            self.spawned_count += 1
            
            # 敏捷型喪屍具備高速追擊能力
            spd = random.uniform(140.0, 185.0)
            self.zombies.append({
                'id': self.zombie_id_counter,
                'x': sx,
                'y': sy,
                'hp': 40,
                'max_hp': 40,
                'speed': spd,
                'hurt_timer': 0.0
            })

        def shoot_bullet(self):
            if self.state != 'playing':
                return
            now = time.time()
            if now - self.last_shot_time < self.shot_cooldown:
                return
            self.last_shot_time = now
            
            # 槍管發射位置 (偏離中心以符合槍口位置)
            bx = self.player_x + (25.0 * self.facing)
            by = self.player_y - 10.0
            
            bullet_speed = 850.0
            vx = math.cos(self.aim_angle) * bullet_speed
            vy = math.sin(self.aim_angle) * bullet_speed
            
            self.bullets.append({
                'x': bx,
                'y': by,
                'vx': vx,
                'vy': vy,
                'life': 1.6
            })
            
            # 槍口微弱火花
            self.particles.append({
                'x': bx,
                'y': by,
                'vx': math.cos(self.aim_angle) * 80.0 + random.uniform(-20, 20),
                'vy': math.sin(self.aim_angle) * 80.0 + random.uniform(-20, 20),
                'life': 0.12,
                'type': 'spark'
            })
            
            # 播放射擊音效 (若存在)
            if renpy.loadable("audio/laser.ogg"):
                renpy.sound.play("audio/laser.ogg")

        def melee_attack(self):
            if self.state != 'playing':
                return
            now = time.time()
            if now - self.last_melee_time < self.melee_cooldown:
                return
            self.last_melee_time = now
            
            # 斬擊範圍 (扇形/圓形範圍中心)
            slash_dist = 45.0
            sx = self.player_x + math.cos(self.aim_angle) * slash_dist
            sy = self.player_y + math.sin(self.aim_angle) * slash_dist
            
            # 斬擊特效
            self.particles.append({
                'x': sx,
                'y': sy,
                'vx': math.cos(self.aim_angle) * 20.0,
                'vy': math.sin(self.aim_angle) * 20.0,
                'life': 0.2,
                'type': 'slash'
            })
            
            # 檢測範圍內的殭屍
            for z in self.zombies:
                dist = math.hypot(z['x'] - sx, z['y'] - sy)
                if dist < 85.0:
                    dmg = 50
                    z['hp'] -= dmg
                    z['hurt_timer'] = 0.35
                    
                    # 近戰強力擊退
                    z['x'] += math.cos(self.aim_angle) * 60.0
                    z['y'] += math.sin(self.aim_angle) * 60.0
                    
                    self.add_floating_text(f"⚔️ -{dmg} 斬擊!", z['x'], z['y'], color="#ffaa00", size=26)
                    self.add_blood_particles(z['x'], z['y'], count=12)
                    
                    if z['hp'] <= 0:
                        self.kills += 1
                        self.add_blood_particles(z['x'], z['y'], count=20)
                        self.add_floating_text("💥 斬殺！+40 EXP", z['x'], z['y'] - 20, color="#00ffff", size=24)

        def add_floating_text(self, text, x, y, color="#ffff00", size=22):
            disp = Text(text, size=size, color=color, bold=True, outlines=[(2, "#000000", 0, 0)])
            self.floating_texts.append({
                'disp': disp,
                'x': x + random.uniform(-10, 10),
                'y': y - 20,
                'vy': -45.0,
                'life': 0.75
            })

        def add_blood_particles(self, x, y, count=8):
            for _ in range(count):
                ang = random.uniform(0, math.pi * 2)
                spd = random.uniform(50.0, 240.0)
                self.particles.append({
                    'x': x,
                    'y': y,
                    'vx': math.cos(ang) * spd,
                    'vy': math.sin(ang) * spd,
                    'life': random.uniform(0.2, 0.45),
                    'type': 'blood'
                })

        def is_inside_room(self, x, y):
            # 菱形四條邊界公式 (中心 1920, 1150 / 半寬 2064 / 半高 1068) -> (原 1720x890 等比例放大 1.2 倍)
            norm_x = abs(x - 1920.0) / 2064.0
            norm_y = abs(y - 1150.0) / 1068.0
            if (norm_x + norm_y) <= 1.0:
                return True
                
            # 如果不在菱形內，判斷是否靠近四個門 (門的通道寬容區)
            for d in self.doors.values():
                if abs(x - d['x']) < 150.0 and abs(y - d['y']) < 150.0:
                    return True
            return False

        def update(self, dt):
            if self.state != 'playing':
                return

            # 熱修復：若從舊存檔讀取，自動套用新版設定
            if not hasattr(self, 'current_room') or 'northwest' not in self.doors:
                self.current_room = getattr(self, 'current_room', 'zombieroom')
                self.doors = {
                    'northwest': {'x': 880.0,  'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'northwest_area', 'spawn_at': 'southeast'},
                    'northeast': {'x': 2960.0, 'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'labortary1',     'spawn_at': 'southwest'},
                    'southwest': {'x': 880.0,  'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southwest_area', 'spawn_at': 'northeast'},
                    'southeast': {'x': 2960.0, 'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southeast_area', 'spawn_at': 'northwest'}
                }
                self.black_bg = Solid("#000000")
                self.door_disp = Solid("#00ffff66")

            # -------------------------------------------------------------
            # 1. 玩家移動計算 (WASD / 方向鍵)
            # -------------------------------------------------------------
            dx = 0.0
            dy = 0.0
            
            # 鍵盤狀態即時讀取 (繞過 Ren'Py 的 Focus 限制)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1.0
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1.0
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1.0
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1.0
                
            # 斜向移動速度歸一化
            if dx != 0.0 and dy != 0.0:
                dx *= 0.7071
                dy *= 0.7071
                
            new_x = self.player_x + dx * self.player_speed * dt
            new_y = self.player_y + dy * self.player_speed * dt
            
            # 使用精確的等角菱形邊界 (Isometric Diamond) 取代原本的方形邊界
            if self.is_inside_room(new_x, new_y):
                self.player_x = new_x
                self.player_y = new_y
            else:
                # 滑牆處理 (Sliding collision)
                if self.is_inside_room(new_x, self.player_y):
                    self.player_x = new_x
                elif self.is_inside_room(self.player_x, new_y):
                    self.player_y = new_y
            
            # 傳送門碰撞偵測 (房間跳轉)
            for d_name, d in self.doors.items():
                if d['target_room'] != self.current_room:  # 只有指向其他房間的門才會觸發
                    if abs(self.player_x - d['x']) < d['w'] / 2 and abs(self.player_y - d['y']) < d['h'] / 2:
                        self.current_room = d['target_room']
                        if self.current_room == 'labortary1':
                            self.bg_disp = Transform("images/labortary1.jpg", xsize=3840, ysize=2160)
                        else:
                            self.bg_disp = Transform("images/zombieroom.jpg", xsize=3840, ysize=2160)
                            
                        target = self.doors[d['spawn_at']]
                        
                        if d['spawn_at'] == 'northwest':
                            self.player_x, self.player_y = target['x'] + 100, target['y'] + 100
                        elif d['spawn_at'] == 'northeast':
                            self.player_x, self.player_y = target['x'] - 100, target['y'] + 100
                        elif d['spawn_at'] == 'southwest':
                            self.player_x, self.player_y = target['x'] + 100, target['y'] - 100
                        elif d['spawn_at'] == 'southeast':
                            self.player_x, self.player_y = target['x'] - 100, target['y'] - 100

                        # 清空當前房間的威脅
                        self.zombies.clear()
                        self.bullets.clear()
                        self.particles.clear()
                        
                        self.screen_hurt_vignette = 0.4
                        self.add_floating_text(f"🚀 進入區域：{self.current_room}", self.player_x, self.player_y - 100, color="#00ff00", size=30)
                        
                        # 立即刷新相機
                        self.cam_x = max(0.0, min(self.map_w - 1920.0, self.player_x - 1920.0 / 2))
                        self.cam_y = max(0.0, min(self.map_h - 1080.0, self.player_y - 1080.0 / 2))
                        break  # 一次只處理一個傳送
            
            # 即時計算攝影機座標 (跟隨玩家並將玩家置中，受限於地圖邊界)
            self.cam_x = max(0.0, min(self.map_w - 1920.0, self.player_x - 1920.0 / 2))
            self.cam_y = max(0.0, min(self.map_h - 1080.0, self.player_y - 1080.0 / 2))
            
            # 無敵與受傷時間遞減
            if self.player_iframes > 0.0:
                self.player_iframes = max(0.0, self.player_iframes - dt)
            if self.screen_shake > 0.0:
                self.screen_shake = max(0.0, self.screen_shake - dt)
            if self.screen_hurt_vignette > 0.0:
                self.screen_hurt_vignette = max(0.0, self.screen_hurt_vignette - dt)

            # -------------------------------------------------------------
            # 2. 自動按住空白鍵連射支援
            # -------------------------------------------------------------
            if keys[pygame.K_SPACE] or keys[pygame.K_j] or keys[pygame.K_k]:
                self.shoot_bullet()

            # -------------------------------------------------------------
            # 3. 子彈飛行與生命週期
            # -------------------------------------------------------------
            active_bullets = []
            for b in self.bullets:
                b['x'] += b['vx'] * dt
                b['y'] += b['vy'] * dt
                b['life'] -= dt
                # 飛出地圖外自動消亡
                if -200 < b['x'] < self.map_w + 200 and -200 < b['y'] < self.map_h + 200 and b['life'] > 0:
                    active_bullets.append(b)
            self.bullets = active_bullets

            # -------------------------------------------------------------
            # 4. 怪物生成波次
            # -------------------------------------------------------------
            now = time.time()
            if now - self.last_spawn_time > self.spawn_interval:
                self.last_spawn_time = now
                if len(self.zombies) < self.max_active_zombies and (self.kills + len(self.zombies)) < self.target_kills:
                    self.spawn_zombie()

            # -------------------------------------------------------------
            # 5. 怪物追蹤與子彈擊中碰撞檢定
            # -------------------------------------------------------------
            active_zombies = []
            for z in self.zombies:
                if z['hp'] <= 0:
                    continue
                    
                if z['hurt_timer'] > 0.0:
                    z['hurt_timer'] = max(0.0, z['hurt_timer'] - dt)
                    
                # 朝玩家追蹤移動 (受擊時速度減半硬直)
                slow_factor = 0.4 if z['hurt_timer'] > 0.0 else 1.0
                z_dx = self.player_x - z['x']
                z_dy = self.player_y - z['y']
                dist_to_p = math.hypot(z_dx, z_dy)
                
                if dist_to_p > 5.0:
                    z['x'] += (z_dx / dist_to_p) * z['speed'] * slow_factor * dt
                    z['y'] += (z_dy / dist_to_p) * z['speed'] * slow_factor * dt

                # 子彈射擊擊中檢定 (距離 < 45px)
                z_dead = False
                for b in list(self.bullets):
                    dist_b = math.hypot(b['x'] - z['x'], b['y'] - z['y'])
                    if dist_b < 45.0:
                        # 移除子彈
                        if b in self.bullets:
                            self.bullets.remove(b)
                            
                        # 命中傷害計算 (20% 機率暴擊)
                        is_crit = (random.random() < 0.25)
                        dmg = 35 if is_crit else 20
                        z['hp'] -= dmg
                        z['hurt_timer'] = 0.16
                        
                        # 擊退效果
                        push_angle = math.atan2(b['vy'], b['vx'])
                        z['x'] += math.cos(push_angle) * 22.0
                        z['y'] += math.sin(push_angle) * 22.0
                        
                        # 浮動傷害數字
                        c_color = "#ffdd00" if is_crit else "#ff4444"
                        crit_str = " (CRIT!)" if is_crit else ""
                        self.add_floating_text(f"-{dmg}{crit_str}", z['x'], z['y'], color=c_color, size=24 if is_crit else 20)
                        self.add_blood_particles(z['x'], z['y'], count=6)
                        
                        # 死亡檢查
                        if z['hp'] <= 0:
                            z_dead = True
                            self.kills += 1
                            self.add_blood_particles(z['x'], z['y'], count=16)
                            self.add_floating_text("💥 殲滅！+40 EXP", z['x'], z['y'] - 20, color="#00ffff", size=22)
                            break
                            
                if z_dead:
                    continue

                # -------------------------------------------------------------
                # 6. 怪物與玩家肉體碰撞檢定 (碰撞受傷效果)
                # -------------------------------------------------------------
                if dist_to_p < 55.0 and self.player_iframes <= 0.0:
                    dmg_p = 15
                    self.player_hp = max(0, self.player_hp - dmg_p)
                    self.player_iframes = 0.8        # 0.8秒無敵時間防止連續暴斃
                    self.screen_shake = 0.35         # 劇烈震屏
                    self.screen_hurt_vignette = 0.45 # 全螢幕猩紅血光
                    
                    # 玩家受創擊退
                    p_push_x = (z_dx / dist_to_p) * -40.0 if dist_to_p > 0 else 0
                    p_push_y = (z_dy / dist_to_p) * -40.0 if dist_to_p > 0 else 0
                    self.player_x += p_push_x
                    self.player_y += p_push_y
                    
                    # 浮動傷害標籤
                    self.add_floating_text(f"⚠️ 咬傷 -{dmg_p} HP!", self.player_x, self.player_y - 30, color="#ff0044", size=25)
                    self.add_blood_particles(self.player_x, self.player_y, count=10)
                    
                    if self.player_hp <= 0:
                        if self.state != 'lost':
                            self.state = 'lost'
                            self.needs_restart = True

                active_zombies.append(z)
                
            self.zombies = active_zombies

            # -------------------------------------------------------------
            # 7. 浮動文字與粒子動畫遞減
            # -------------------------------------------------------------
            active_texts = []
            for ft in self.floating_texts:
                ft['y'] += ft['vy'] * dt
                ft['life'] -= dt
                if ft['life'] > 0.0:
                    active_texts.append(ft)
            self.floating_texts = active_texts
            
            active_particles = []
            for p in self.particles:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['life'] -= dt
                if p['life'] > 0.0:
                    active_particles.append(p)
            self.particles = active_particles

            # -------------------------------------------------------------
            # 8. 勝利條件判定 (擊殺達標)
            # -------------------------------------------------------------
            if self.kills >= self.target_kills and self.state == 'playing':
                self.state = 'won'
                self.needs_restart = True

        def render(self, width, height, st, at):
            r = renpy.Render(width, height)

            # 熱修復：確保反序列化舊存檔時所有屬性完備
            if not hasattr(self, 'black_bg'):
                self.black_bg = Solid("#000000")
            if not hasattr(self, 'door_disp'):
                self.door_disp = Solid("#00ffff66")
            if not hasattr(self, 'doors') or 'northwest' not in self.doors:
                self.current_room = getattr(self, 'current_room', 'zombieroom')
                self.doors = {
                    'northwest': {'x': 880.0,  'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'northwest_area', 'spawn_at': 'southeast'},
                    'northeast': {'x': 2960.0, 'y': 720.0,  'w': 220.0, 'h': 220.0, 'target_room': 'labortary1',     'spawn_at': 'southwest'},
                    'southwest': {'x': 880.0,  'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southwest_area', 'spawn_at': 'northeast'},
                    'southeast': {'x': 2960.0, 'y': 1580.0, 'w': 220.0, 'h': 220.0, 'target_room': 'southeast_area', 'spawn_at': 'northwest'}
                }

            # 計算時間增量 (dt) 用於物理運算
            if self.last_st is None:
                dt = 0.016
            else:
                dt = max(0.001, min(0.1, st - self.last_st))
            self.last_st = st

            # 驅動主邏輯更新
            self.update(dt)

            # 震屏偏移
            ox = 0
            oy = 0
            if self.screen_shake > 0.0:
                ox = random.randint(-8, 8)
                oy = random.randint(-8, 8)

            # 0. 繪製純黑遮罩 (防漏底)
            r.blit(renpy.render(BATTLE_BLACK_BG, width, height, st, at), (0, 0))

            # 1. 繪製背景 (居中對齊於世界地圖 + 攝影機位移)
            bg_r = renpy.render(self.bg_disp, 3840, 2160, st, at)
            bg_w, bg_h = bg_r.get_size()
            bg_x = int((self.map_w - bg_w) / 2.0 - self.cam_x + ox)
            bg_y = int((self.map_h - bg_h) / 2.0 - self.cam_y + oy)
            r.blit(bg_r, (bg_x, bg_y))

            # 1.5 繪製傳送門 (發光的邊界區域，只顯示可用的傳送門)
            for d_name, d in self.doors.items():
                if d['target_room'] != self.current_room:
                    door_r = renpy.render(BATTLE_DOOR_DISP, d['w'], d['h'], st, at)
                    r.blit(door_r, (int(d['x'] - d['w']/2 - self.cam_x + ox), int(d['y'] - d['h']/2 - self.cam_y + oy)))

            # 2. 繪製子彈
            for b in self.bullets:
                br = renpy.render(self.bullet_disp, width, height, st, at)
                r.blit(br, (int(b['x'] - self.cam_x + ox - 6), int(b['y'] - self.cam_y + oy - 6)))

            # 3. 繪製粒子效果
            for p in self.particles:
                p_disp = self.spark_disp if p.get('type') == 'spark' else self.particle_disp
                pr = renpy.render(p_disp, width, height, st, at)
                r.blit(pr, (int(p['x'] - self.cam_x + ox - 4), int(p['y'] - self.cam_y + oy - 4)))

            # 4. 繪製敏捷型喪屍 (agile_zombie)
            for z in self.zombies:
                z_disp = self.red_flash if z['hurt_timer'] > 0.0 else self.zombie_normal
                zr = renpy.render(z_disp, width, height, st, at)
                r.blit(zr, (int(z['x'] - self.cam_x + ox - 40), int(z['y'] - self.cam_y + oy - 40)))

                # 怪物上方頭頂動態血條
                hp_pct = max(0.0, min(1.0, float(z['hp']) / float(z['max_hp'])))
                hp_w = max(1, int(60 * hp_pct))
                bg_bar = renpy.render(self.hp_bar_bg, 60, 7, st, at)
                r.blit(bg_bar, (int(z['x'] - self.cam_x + ox - 30), int(z['y'] - self.cam_y + oy - 50)))
                bar_fg = self.hp_bar_danger if hp_pct < 0.35 else self.hp_bar_fg
                fg_r = renpy.render(bar_fg, hp_w, 7, st, at)
                r.blit(fg_r, (int(z['x'] - self.cam_x + ox - 30), int(z['y'] - self.cam_y + oy - 50)))

            # 5. 繪製玩家 (依朝向選用左右精靈，無敵時閃爍)
            p_disp = self.player_right if self.facing == 1 else self.player_left
            is_blink_hidden = (self.player_iframes > 0.0 and int(st * 16) % 2 == 0)
            if not is_blink_hidden:
                pr = renpy.render(p_disp, width, height, st, at)
                r.blit(pr, (int(self.player_x - self.cam_x + ox - 40), int(self.player_y - self.cam_y + oy - 57)))

            # 6. 瞄準指示光點
            aim_len = 65.0
            ax = int(self.player_x - self.cam_x + ox + math.cos(self.aim_angle) * aim_len)
            ay = int(self.player_y - self.cam_y + oy + math.sin(self.aim_angle) * aim_len)
            aim_r = renpy.render(self.bullet_disp, width, height, st, at)
            r.blit(aim_r, (ax - 6, ay - 6))

            # 7. 浮動傷害數字
            for ft in self.floating_texts:
                tr = renpy.render(ft['disp'], width, height, st, at)
                r.blit(tr, (int(ft['x'] - self.cam_x + ox), int(ft['y'] - self.cam_y + oy)))

            # 8. 全螢幕受傷猩紅血光遮罩 (固定在螢幕上不跟隨相機)
            if self.screen_hurt_vignette > 0.0:
                vr = renpy.render(self.screen_hurt_disp, width, height, st, at)
                r.blit(vr, (0, 0))

            # 請求 60 FPS 平滑重繪
            renpy.redraw(self, 0.016)
            return r

        def event(self, ev, x, y, st):
            if getattr(self, 'needs_restart', False):
                self.needs_restart = False
                renpy.restart_interaction()
                
            # 將螢幕滑鼠座標轉為世界座標
            world_mouse_x = x + self.cam_x
            world_mouse_y = y + self.cam_y

            if ev.type == pygame.MOUSEMOTION:
                self.mouse_x = world_mouse_x
                self.mouse_y = world_mouse_y
                self.aim_angle = math.atan2(world_mouse_y - self.player_y, world_mouse_x - self.player_x)
                self.facing = -1 if math.cos(self.aim_angle) < 0 else 1

            elif ev.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_x = world_mouse_x
                self.mouse_y = world_mouse_y
                self.aim_angle = math.atan2(world_mouse_y - self.player_y, world_mouse_x - self.player_x)
                self.facing = -1 if math.cos(self.aim_angle) < 0 else 1
                
                if ev.button == 1:
                    self.melee_attack()
                    raise renpy.IgnoreEvent()
                elif ev.button == 3:
                    self.shoot_bullet()
                    raise renpy.IgnoreEvent()

        def visit(self):
            return [
                self.bg_disp, self.player_right, self.player_left, self.zombie_normal,
                self.red_flash, self.screen_hurt_disp, self.bullet_disp, self.particle_disp,
                self.spark_disp, self.hp_bar_bg, self.hp_bar_fg, self.hp_bar_danger
            ]

# ==============================================================================
# 即時戰鬥外層 Screen (HUD 資訊面板、觸控按鈕與結算視窗)
# ==============================================================================
default active_battlefield_displayable = None

screen action_zombie_battle_screen(target_kills=8):
    modal True

    # 底層加上純黑背景，徹底防範畫面震動或縮放時出現漏底 (穿過底層的 zombie_street)
    add Solid("#000000")

    # 禁用可能干擾 WASD 移動與戰鬥的 Ren'Py 預設快捷鍵 (例如 S 截圖、D 導演、選單等)
    key "game_menu" action NullAction()
    key "screenshot" action NullAction()
    key "director" action NullAction()
    key "accessibility" action NullAction()
    key "s" action NullAction()
    key "S" action NullAction()
    key "a" action NullAction()
    key "A" action NullAction()
    key "d" action NullAction()
    key "D" action NullAction()
    key "w" action NullAction()
    key "W" action NullAction()

    # 確保 Displayable 正確初始化並維持狀態
    default battle_core = ActionZombieBattleDisplayable(target_kills=target_kills)

    # 核心 60FPS 畫布
    add battle_core

    # -------------------------------------------------------------
    # 頂部戰術 HUD (血條、進度、操作提示)
    # -------------------------------------------------------------
    frame:
        xalign 0.5 ypos 20
        xysize (1820, 85)
        background "#091224ee"
        padding (25, 12)

        hbox:
            spacing 40
            yalign 0.5

            # 玩家生命值
            hbox:
                spacing 15
                yalign 0.5
                text "顧臨淵 HP：" size 17 color "#00ffff" bold True yalign 0.5
                $ p_hp = max(0, battle_core.player_hp)
                $ p_bar_w = int(240 * (float(p_hp) / float(battle_core.player_max_hp)))
                frame:
                    xysize (240, 24)
                    background "#330000"
                    padding (0, 0)
                    yalign 0.5
                    frame:
                        xysize (p_bar_w, 24)
                        background ("#00ff66" if p_hp > 40 else "#ff3333")
                        padding (0, 0)
                text f"{p_hp} / {battle_core.player_max_hp}" size 16 color "#ffffff" bold True yalign 0.5

            # 殲滅目標計數
            hbox:
                spacing 15
                yalign 0.5
                text "☣️ 敏捷型喪屍目標：" size 17 color "#ffaa00" bold True yalign 0.5
                text f"已擊斃 {battle_core.kills} / {battle_core.target_kills} 隻" size 20 color "#ff3333" bold True yalign 0.5

            # 操作提示
            hbox:
                spacing 10
                text "【WASD/方向鍵】四向移動 ｜【滑鼠左鍵】近戰斬殺 ｜【滑鼠右鍵/空白鍵】遠程射擊" size 14 color "#aaaaaa" yalign 0.5

    # -------------------------------------------------------------
    # 底部輔助按鈕 (供滑鼠 / 觸控點選使用)
    # -------------------------------------------------------------
    frame:
        align (0.95, 0.95)
        xysize (240, 75)
        background "#ff2222cc"
        padding (10, 10)
        button:
            xfill True yfill True
            action Function(battle_core.shoot_bullet)
            text "💥 扣動扳機開火 (FIRE)" size 17 color "#ffffff" bold True align (0.5, 0.5)

    # -------------------------------------------------------------
    # 勝利結算浮動視窗
    # -------------------------------------------------------------
    if battle_core.state == 'won':
        frame:
            modal True
            align (0.5, 0.5)
            xysize (750, 420)
            background "#05182aee"
            padding (40, 35)

            vbox:
                spacing 20
                xalign 0.5 yalign 0.5

                text "🎉【生化隔離大廳 · 突圍大捷！】" size 28 color "#00ffcc" bold True xalign 0.5
                text "地下 B1 涌入的敏捷型喪屍先鋒部隊已被全數殲滅！\n刺鼻的硝煙散去，防爆密封門前的安全威脅已暫時排除。" size 16 color "#dddddd" xalign 0.5 text_align 0.5

                frame:
                    xalign 0.5
                    xysize (620, 60)
                    background "#102336dd"
                    text "戰鬥戰果：+300 點生存點數 ｜ +150 點角色經驗值 (EXP)" size 16 color "#ffcc00" bold True align (0.5, 0.5)

                null height 10
                button:
                    xalign 0.5
                    xysize (450, 60)
                    background "#0088cc"
                    hover_background "#00aaff"
                    action Return("win")
                    text "【 ⚔️ 重整隊列 · 繼續深入設施 ➔ 】" size 18 color "#ffffff" bold True align (0.5, 0.5)

    # -------------------------------------------------------------
    # 失敗結算浮動視窗
    # -------------------------------------------------------------
    elif battle_core.state == 'lost':
        frame:
            modal True
            align (0.5, 0.5)
            xysize (750, 420)
            background "#26060bee"
            padding (40, 35)

            vbox:
                spacing 20
                xalign 0.5 yalign 0.5

                text "💀【防線告急 · 遭受致命撲咬！】" size 28 color "#ff3333" bold True xalign 0.5
                text "敏捷型感染體以恐怖的速度突破了你的防禦死角，\n利爪撕裂了單兵防護服！" size 16 color "#dddddd" xalign 0.5 text_align 0.5

                null height 15
                hbox:
                    spacing 30
                    xalign 0.5

                    button:
                        xysize (280, 60)
                        background "#b82a2a"
                        hover_background "#e63939"
                        action Function(battle_core.reset_game)
                        text "【 🔄 重新突圍挑戰 】" size 16 color "#ffffff" bold True align (0.5, 0.5)

                    button:
                        xysize (280, 60)
                        background "#334466"
                        hover_background "#445588"
                        action Return("skip")
                        text "【 🛡️ 冷月雙槍火力掩護 】" size 16 color "#aaccff" bold True align (0.5, 0.5)
