# 📜 《輪迴世界》開發規格書 - 06: AI 視覺生成咒文庫 (Prompt Library)

本文件提供《輪迴世界》所需的 UI 介面、副本探索地圖、血統特效，以及 **10 張不同職階的角色頭像照片 (Portraits)** 之 AI 繪圖提示詞（Prompt）與程式載入規範。

---

## 1. 角色頭像系統與顯示規範 (Avatar System Specifications)

開發程式或寫入 JSON 數據庫時，請遵守以下頭像顯示邏輯：

1. **圖像格式規範：** 所有角色頭像統一採用 **1:1 正方形比例 (`--ar 1:1`)**、**角色近景頭像 (Face Portrait / Headshot)** 與 **暗黑美漫/韓漫精緻風格**，確保視覺風格一致。
2. **三 UI 畫面自動渲染：** JSON 中的 `portrait` 檔名變數必須自動串接並顯示於以下三個介面：
   * **對話介面 (Dialogue UI):** 對話框邊角顯示當前發言角色的頭像。
   * **戰鬥介面 (Combat UI):** 前後排血條與行動順序欄旁顯示角色頭像。
   * **列表介面 (Party List UI):** 隊伍名冊、後勤招募與個人房間狀態欄顯示角色頭像。

---

## 2. 10 張預設角色頭像照片提示詞 (Character Portraits)

### 🛡️ 1. 坦克 (男性) — `portrait_tank_m.png`
> **Prompt:**
> Game avatar portrait, male heavy tank warrior, tough rugged veteran, wearing dark tactical exoskeleton armor with heavy shoulder pads, scar on cheek, stern expression, dark gritty sci-fi background, high detail anime style, 2d game art, headshot --ar 1:1

### 🛡️ 2. 坦克 (女性) — `portrait_tank_f.png`
> **Prompt:**
> Game avatar portrait, female defender tank, short dark hair, wearing heavy polished steel and carbon fiber chestplate, calm resolute gaze, subtle glowing energy shield in background, anime art style, 2d game icon, headshot --ar 1:1

### 🧠 3. 智者 (男性) — `portrait_scholar_m.png`
> **Prompt:**
> Game avatar portrait, male intelligent scholar strategist, wearing round glasses, slicked back hair, sharp analytical eyes, wearing a sleek high-tech coat, holographic data floating around, anime art style, headshot --ar 1:1

### 🧠 4. 智者 (女性) — `portrait_scholar_f.png`
> **Prompt:**
> Game avatar portrait, female genius hacker scholar, wearing high-tech earpiece and dark blue coat, perceptive eyes, silver hair in a ponytail, blue glowing code lines in dark background, anime art style, headshot --ar 1:1

### ⚔️ 5. 輸出手/槍手 (男性) — `portrait_attacker_m.png`
> **Prompt:**
> Game avatar portrait, male dangerous sharpshooter attacker, messy hair, confident smirk, wearing tactical leather jacket with ammo belt across chest, red lens goggles on forehead, dark sci-fi background, anime art style, headshot --ar 1:1

### ⚔️ 6. 輸出手/刀客 (女性) — `portrait_attacker_f.png`
> **Prompt:**
> Game avatar portrait, female deadly assault swordswoman, crimson eyes, ponytail hair, holding high-frequency blade near shoulder, fierce determined expression, dark cyberpunk atmosphere, anime art style, headshot --ar 1:1

### 🚬 7. 流氓/街匪 (男性) — `portrait_rogue_m.png`
> **Prompt:**
> Game avatar portrait, male cynical rogue street thug, cigarette in mouth, tattoos on neck, wild hair, dark hoody, edgy rebellious expression, dimly lit alleyway background, anime art style, headshot --ar 1:1

### 🗡️ 8. 刺客/影子 (女性) — `portrait_assassin_f.png`
> **Prompt:**
> Game avatar portrait, female shadow assassin, wearing dark facemask covering lower face, piercing glowing yellow eyes, dark hood, holding a glowing tactical kunai, dark purple mist background, anime art style, headshot --ar 1:1

### 💉 9. 戰術醫護兵 (女性) — `portrait_medic_f.png`
> **Prompt:**
> Game avatar portrait, female field combat medic, wearing white and blue tactical medical gear with cross insignia, gentle yet focused expression, glowing green healing energy in hand, anime art style, headshot --ar 1:1

### ⚙️ 10. 科技專家/機械師 (男性) — `portrait_engineer_m.png`
> **Prompt:**
> Game avatar portrait, male expert combat engineer mechanic, wearing welder goggles raised on forehead, grease stain on cheek, holding a high-tech wrench, mischievous confident smile, sparks background, anime art style, headshot --ar 1:1

---

## 3. 樞紐與 UI 介面 (Hub & UI Assets)

### 🌌 虛空大廳 (Void Hall / main_room.rpy 背景)
> **Prompt:** 
> Anime concept art of a futuristic dark sanctuary, Void Hall, a massive hovering glowing blue energy crystal in the center, obsidian floor with glowing circuit lines, cosmic starry sky background, mysterious atmosphere --ar 16:9

### 📜 命運碎片圖示 (Fate Shard Icon)
> **Prompt:** 
> Game item icon, a glowing sharp crystal shard floating, dark cosmic magic energy surrounding it, isolated on black background, 2d game UI asset, vector style --ar 1:1

---

## 4. 五大副本探索地圖 (Campaign Map Environments)

* **🟢 1. 喪屍末日世界 (Zombie World):** `Dark sci-fi underground research facility, green toxic fog leaking from broken pipes, emergency red lights flashing --ar 16:9`
* **🔵 2. 太空真空世界 (Space World):** `Interior of a derelict spaceship, zero gravity environment, floating debris, metallic corridor, dim blue neon lights --ar 16:9`
* **🟣 3. 靈異鬼怪世界 (Paranormal World):** `Abandoned Japanese city street at midnight, heavy creepy purple fog, ghost paper lanterns glowing --ar 16:9`
* **🟡 4. 古文明魔法世界 (Magic World):** `Interior of an ancient Egyptian pyramid chamber, glowing golden hieroglyphs, magical blue orbs --ar 16:9`
* **🔴 5. 因果律世界 (Causality World):** `Rainy modern city street at twilight, chaotic traffic accident in slow motion, dark shadow of Death looming --ar 16:9`

---

## 5. 血統與特效概念 (Bloodlines & Effects)

* **🪽 天使血統:** `Character splash art, warrior with six glowing holy white feather wings, divine golden aura --ar 3:4`
* **🦇 惡魔血統:** `Character splash art, dark warrior with black demon bat wings, crimson horn, dark fire burning --ar 3:4`
* **🛹 綠魔滑板:** `Futuristic high-tech hoverboard, metallic green armor, glowing jet thrusters, 2d game asset --ar 1:1`