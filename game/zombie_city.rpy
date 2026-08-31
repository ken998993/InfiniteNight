# ==============================================================================
# 📜 《輪迴世界》第一副本：喪屍末日世界 · 極光重工遺址 (zombie_city.rpy)
# 依據 developMd/09_Story_Stage_1_1_Zombie_City.md 規範重構
# ==============================================================================

# 定義關卡專屬角色對話物件
define lengyue = Character("冷月", color="#00ffcc", image="lengyue")
define xiangtian = Character("項天", color="#ff8844", image="xiangtian")
define suxiao = Character("蘇曉", color="#66ccff", image="suxiao")
define gulin = Character("顧臨淵", color="#00ffea")
define zhao_hu = Character("趙虎 (刺青流氓)", color="#ff6666", image="zhao_hu")
define zhou_yang = Character("周揚 (驚慌青年)", color="#bbbbbb", image="zhou_yang")
define qian_fugui = Character("錢富貴 (大叔)", color="#aaaaaa", image="qian_fugui")
define aurora_captain = Character("極光重工安保隊長", color="#ffaa00", image="aurora_captain")
define adam_ai = Character("A.D.A.M. 核心主機", color="#ddaaff", image="adam_ai")

# 定義常用特殊轉場特效
define flash = Fade(0.1, 0.0, 0.3, color="#ffffff")
define flash_red = Fade(0.1, 0.0, 0.3, color="#ff0000")

# 定義關卡背景圖元別名 (全圖縮放拉滿 1920x1080，消除黑邊與馬賽克邊)
image bg_aurora_lab_entrance = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_aurora_corridor = Transform("images/zombie_street.PNG", xsize=1920, ysize=1080)
image bg_aurora_core = Transform("images/adamcore.jpg", xsize=1920, ysize=1080)

# ==========================================
# 關卡進入點 (相容 zombieCity 與 stage_1_1)
# ==========================================
# 🗺️ 第一關劇情模式專屬點擊式戰術地圖 (方案 2)
# 採用 16:9 地下設施戰術俯瞰地圖，提供毀滅戰士 / 暗黑地牢風格的點選體驗
# ==========================================
screen stage_1_1_tactical_map_screen(current_step=1):
    modal True

    # 1. 戰術全息俯瞰底圖
    add "images/zombieCityMap.jpg" xsize 1920 ysize 1080

    # 暗黑全息半透明遮罩
    frame:
        background "#050b18ea"
        xsize 1920 ysize 1080

    # 2. 頂部任務進度與戰術標題
    frame:
        xalign 0.5 ypos 30
        xysize (1800, 95)
        background "#081426f0"
        padding (30, 15)

        vbox:
            spacing 6
            text "【 🗺️ 極光重工地下生化研發中心 · 戰術行進藍圖 (戰術選擇模式) 】" size 22 color "#00ffff" bold True
            hbox:
                spacing 20
                text f"📍 當前推進進度：階段 {current_step} / 3" size 16 color "#ffcc00" bold True
                text "• 點擊當前開放的區域節點，引導小隊突破生化封鎖！" size 15 color "#aaaaaa"

    # 3. 三大核心區域戰術卡片
    hbox:
        xalign 0.5 ypos 160
        spacing 35

        # -------------------------------------------------------------
        # 節點 1: 🚪 B1 生化隔離防爆大門 (Wave 1 戰鬥)
        # -------------------------------------------------------------
        frame:
            xysize (550, 840)
            background ("#1a2436f5" if current_step == 1 else ("#0f1724dd" if current_step > 1 else "#090e18dd"))
            padding (25, 25)

            vbox:
                spacing 15
                xfill True

                hbox:
                    spacing 10
                    text "🚪" size 30 yalign 0.5
                    text "區域一：生化隔離防爆大門" size 20 color "#ffffff" bold True yalign 0.5

                if current_step == 1:
                    text "【 📍 當前突入目標 】" size 16 color "#ff4444" bold True
                else:
                    text "【 ✅ 區域已肅清突破 】" size 16 color "#00ff66" bold True

                # 背景圖片展示區
                frame:
                    xysize (500, 220)
                    background "#000000"
                    add "images/zombie_street.PNG" xsize 500 ysize 220

                # 區域情報
                vbox:
                    spacing 8
                    text "【 📋 戰術情報簡報 】" size 16 color "#00ffff" bold True
                    text "• 設施位置：地下 B1 外圍生化隔離區\n• 環境狀況：金屬閥門遭破壞，重型鎖死防爆門前聚集大量感染體\n• 威脅評估：3 隻高速敏捷型喪屍伺機突襲！" size 14 color "#dddddd"
                    
                    null height 5
                    text "🧟 預計遭遇：敏捷型喪屍 (agile_zombie) x 3" size 14 color "#ff7777" bold True
                    text "🎁 首通獎勵：解鎖戰術服防護、開啟 B2 探索路線" size 13 color "#ffcc00"

                null height 10

                # 行動按鈕
                if current_step == 1:
                    button:
                        xalign 0.5
                        xysize (480, 60)
                        background "#b82a2a"
                        hover_background "#e63939"
                        action Return("node_1")
                        text "【 ⚔️ 突入防爆大門 (進入第一波戰鬥) 】" size 17 color "#ffffff" bold True xalign 0.5 yalign 0.5
                else:
                    frame:
                        xalign 0.5
                        xysize (480, 60)
                        background "#163320dd"
                        text "【 ✅ 該防線已成功突破 】" size 16 color "#00ff66" bold True xalign 0.5 yalign 0.5

        # -------------------------------------------------------------
        # 節點 2: 🛗 B2 廢棄電梯井與主通風管道 (Wave 2 毒氣戰鬥)
        # -------------------------------------------------------------
        frame:
            xysize (550, 840)
            background ("#1a2436f5" if current_step == 2 else ("#0f1724dd" if current_step > 2 else "#090e18dd"))
            padding (25, 25)

            vbox:
                spacing 15
                xfill True

                hbox:
                    spacing 10
                    text "🛗" size 30 yalign 0.5
                    text "區域二：廢棄電梯井與毒氣走廊" size 20 color "#ffffff" bold True yalign 0.5

                if current_step < 2:
                    text "【 🔒 尚未抵達 (需先突破防爆大門) 】" size 16 color "#777777"
                elif current_step == 2:
                    text "【 📍 當前突入目標 】" size 16 color "#ff4444" bold True
                else:
                    text "【 ✅ 區域已穿越肅清 】" size 16 color "#00ff66" bold True

                # 背景圖片展示區
                frame:
                    xysize (500, 220)
                    background "#000000"
                    add "images/zombie_street.PNG" xsize 500 ysize 220

                # 區域情報
                vbox:
                    spacing 8
                    text "【 📋 戰術情報簡報 】" size 16 color "#00ffff" bold True
                    text "• 設施位置：地下 B2 主通風管道走廊\n• 環境危害：高溫黃色生化毒氣洩漏（每回合 -5% HP）\n• 戰術關鍵：密集變異腐屍堵門，需使用高爆手雷清場！" size 14 color "#dddddd"
                    
                    null height 5
                    text "🧟 預計遭遇：變異腐屍 x 3 + 敏捷型喪屍 x 2 (毒氣環境)" size 14 color "#ff7777" bold True
                    text "💣 戰術配給：high_explosive 高爆破片手雷 x 2" size 13 color "#ffcc00"

                null height 10

                # 行動按鈕
                if current_step == 2:
                    button:
                        xalign 0.5
                        xysize (480, 60)
                        background "#b82a2a"
                        hover_background "#e63939"
                        action Return("node_2")
                        text "【 💣 突入毒氣走廊 (投擲手雷清場) 】" size 17 color "#ffffff" bold True xalign 0.5 yalign 0.5
                elif current_step > 2:
                    frame:
                        xalign 0.5
                        xysize (480, 60)
                        background "#163320dd"
                        text "【 ✅ 毒氣走廊已成功穿越 】" size 16 color "#00ff66" bold True xalign 0.5 yalign 0.5
                else:
                    frame:
                        xalign 0.5
                        xysize (480, 60)
                        background "#151c2add"
                        text "【 🔒 請先突破前方防爆大門 】" size 16 color "#666666" bold True xalign 0.5 yalign 0.5

        # -------------------------------------------------------------
        # 節點 3: 🧠 B3 深層生物神經網絡 A.D.A.M. 機房
        # -------------------------------------------------------------
        frame:
            xysize (550, 840)
            background ("#1a2436f5" if current_step == 3 else "#090e18dd")
            padding (25, 25)

            vbox:
                spacing 15
                xfill True

                hbox:
                    spacing 10
                    text "🧠" size 30 yalign 0.5
                    text "區域三：深層神經中樞 A.D.A.M." size 20 color "#ffffff" bold True yalign 0.5

                if current_step < 3:
                    text "【 🔒 尚未抵達 (需先穿越毒氣走廊) 】" size 16 color "#777777"
                else:
                    text "【 📍 最終攻略目標 (智者入侵) 】" size 16 color "#00ffff" bold True

                # 背景圖片展示區
                frame:
                    xysize (500, 220)
                    background "#000000"
                    add "images/adamcore.jpg" xsize 500 ysize 220

                # 區域情報
                vbox:
                    spacing 8
                    text "【 📋 戰術情報簡報 】" size 16 color "#00ffff" bold True
                    text "• 設施位置：地下 B3 生物神經網絡最深層\n• 核心設施：超級電腦 A.D.A.M. 亞當核心主機\n• 關鍵條件：隊伍智力 INT >= 100 可駭入下載完整神經原始碼！" size 14 color "#dddddd"
                    
                    null height 5
                    text "💻 任務目標：下載亞當神經核心 / 引爆主機完成回歸" size 14 color "#66ccff" bold True
                    text "💎 首通大獎：【亞當神經元矩陣備份】、C 階碎片、生存點數" size 13 color "#ffcc00"

                null height 10

                # 行動按鈕
                if current_step == 3:
                    button:
                        xalign 0.5
                        xysize (480, 60)
                        background "#0b6699"
                        hover_background "#1188cc"
                        action Return("node_3")
                        text "【 🧠 進入神經網絡核心 (智者檢定) 】" size 17 color "#ffffff" bold True xalign 0.5 yalign 0.5
                else:
                    frame:
                        xalign 0.5
                        xysize (480, 60)
                        background "#151c2add"
                        text "【 🔒 請先穿越毒氣走廊 】" size 16 color "#666666" bold True xalign 0.5 yalign 0.5


label zombieCity:
    jump stage_1_1_zombie_city

label stage_1_1_zombie_city:
    scene bg_aurora_lab_entrance with fade
    
    # -------------------------------------------------------------
    # 1. 10分鐘保護光幕降臨與新人甦醒 (1 資深者 + 6 互不相識的新人)
    # -------------------------------------------------------------
    n "一陣強烈的時空扭曲與劇烈眩暈感襲來，冰冷潮濕的合金地面刺激著神經，空氣中瀰漫著刺鼻的金屬鏽蝕味與淡淡的腐敗血腥氣息。"
    n "你揉著劇烈疼痛的太陽穴掙扎著坐起身，低頭看向手腕——不知何時，上面多了一只散發著微光的黑色金屬腕錶。"
    n "在你四周，籠罩著一層淡淡的半透明金色光幕，將外面的死寂走廊徹底隔絕。"
    n "身旁躺著幾名同樣剛剛甦醒、穿著普通現代服裝的陌生男女，每個人臉上都寫滿了茫然與驚恐。"
    
    "【輪迴終端冰冷機械音播報】："
    "「——輪迴系統載入完畢。"
    "當前世界：【末日廢墟 · 諾克斯市】"
    "當前位置：極光重工地下生化研究所 B1 外部聯絡站。"
    "新手保護光幕已啟動，剩餘時間：09分59秒。"
    "身份認知覆蓋生效：極光重工安保部 · 第 7 應急支援組。」"
    
    qian_fugui "這……這是哪裡啊？！剛才那陣金光是什麼東西？我明明剛在公司點算貨款啊！"
    
    zhou_yang "（渾身發抖地縮在角落）綁架……是綁架嗎？！求求你們別殺我，我只是個實習生……"
    
    zhao_hu "（滿身刺青的光頭漢子猛地跳起來，暴躁地罵道）操！少裝神弄鬼！老子在道上混了十幾年，誰敢算計老子？！"
    
    xiangtian "（一名身穿工裝夾克、身材結實的青年沉著臉站起身）大家先冷靜一下，看看手腕上的手錶……這東西好像直接連接著我們的神經，不像是普通惡作劇。"
    
    suxiao "（戴著圓框眼鏡、穿著風衣的年輕女子抱著隨身筆記本，臉色蒼白地環顧四周）……空氣裡有生化警示標籤的氣味，這裡的防爆鋼門上寫著『極光重工 · 生化危害 4 級』……這簡直就像我寫的科幻懸疑小說裡的場景……"
    
    show lengyue at center with dissolve
    lengyue "吵夠了沒有？"
    
    n "說話的是一名站在光幕角落的女子。與其他驚慌失措的新人截然不同，她身著俐落的深色戰術背心，戴著通訊耳機，眼神如刀鋒般冰冷，手腕上的腕錶閃爍著深藍光芒。"
    
    lengyue "醒了就都站起來。算上你們，這次一共來了 6 個新面孔。想活命就閉嘴聽我說。"
    lengyue "頭頂這層金色光罩是輪迴空間的『新手保護光幕』，持續十分鐘。在時間歸零前，外界的感染者、毒氣或任何攻擊都穿不透這層膜，但我們也走不出去。"
    lengyue "輪迴系統已經偽造了我們的身份，將我們標記為前來支援的『外包應急小隊』。等一下不管看到什麼，管好你們的嘴，誰敢暴露輪迴空間的秘密，下場就是被系統當場抹殺！"
    hide lengyue with dissolve
    
    gulin "（站起身冷靜地開口）我是顧臨淵。既然我們被困在同一條船上，大家先穩住情緒，觀察周圍情況。"
    
    xiangtian "我叫項天，在機械廠當維修工，有些力氣。"
    
    suxiao "我叫蘇曉……是個全職懸疑小說作家。（扶了扶眼鏡，指向光幕外的濃霧）……大家快看外面！穿過那層黃綠色的濃煙，有三名穿著重型外骨骼裝甲、拿著突擊步槍的人正朝光幕走過來！"
    
    # -------------------------------------------------------------
    # 2. 極光安保隊長（雷恩）登場與斥責
    # -------------------------------------------------------------
    "眾人順著蘇曉手指的方向看去，光幕外沉重的金屬腳步聲由遠及近。"
    "三名身穿重型深藍外骨骼裝甲、頭戴猩紅目鏡的武裝人員快步走來。領頭的正是面帶刀疤、眼神凌厲的極光重工安保隊長——雷恩。"
    "雷恩隊長隔著金色光幕，看著裡面穿著休閒服、工裝、西裝與長裙的眾人，眉頭緊緊擰成了麻花，猛地拍打著光幕邊緣的金屬外框。"
    
    aurora_captain "該死！總部高層到底在搞什麼鬼？！我申請的是『極光重工第一序列重裝特勤組』，怎麼派來你們這群連站都站不穩的二流外包臨時工？！"
    aurora_captain "看看你們那副散漫的樣子！一個拿筆的弱女子、一個發抖的胖子、兩個穿西裝的弱雞！你們以為諾克斯市還是以前那個繁華大都市嗎？聽好了，這裡現在是人間地獄！"
    
    # -------------------------------------------------------------
    # 3. 資深者冷月上前交涉與世界觀深度交代 (Worldbuilding)
    # -------------------------------------------------------------
    show lengyue at center with dissolve
    lengyue "（眼神冰冷，直接上前亮出手腕上的外包應急電子授權碼，語氣沉著俐落）"
    lengyue "我是第 7 應急組帶隊隊長『冷月』。我們在進入地下聯絡站時遭遇了外圍突變體襲擊，部分人員傷亡、情報受阻。"
    lengyue "雷恩隊長，別浪費時間抱怨了。立刻簡報當前地下設施的封鎖現況，我們接到的合約指令是全力配合你殺入深層重啟主機！"
    hide lengyue with dissolve
    
    aurora_captain "（打量著冷月凌厲的戰術身姿與電子授權碼，語氣稍微緩和但依然嚴肅）哼，看來總部至少還派了個像樣的帶隊隊長。聽清楚了，我只說一次："
    
    aurora_captain "【第一，諾克斯市與生化浩劫】。"
    aurora_captain "三天前，諾克斯市的地下水源被不明生化病毒污染，全市九成市民在幾小時內變異成嗜血的狂暴感染者。極光重工啟動了最高緊急隔離條例，用外圍的重裝防爆門把整個城市徹底封鎖成了死城。"
    
    aurora_captain "【第二，地下研究所與失控主機 A.D.A.M.】。"
    aurora_captain "但更致命的在我們腳下！地下最深處的生物超級電腦『A.D.A.M.』判定研究所發生了 7 級生化洩漏，直接啟動了自毀封鎖協議！A.D.A.M. 釋放了神經毒氣，殺死了所有研究員，並將整座設施的各層防爆閘門通通鎖死！"
    
    aurora_captain "【第三，極光畸變體與狂暴屍潮】。"
    aurora_captain "死在毒氣裡的研究員被極光病毒二次感染，變異成了動作極快的『敏捷型喪屍』。那些怪物骨刺外露、能在天花板上攀爬，甚至還保留著生前開啟部分閘門的肌肉記憶！"
    
    # -------------------------------------------------------------
    # 4. 發放 tactical_hazmat_armor 戰術服與著裝
    # -------------------------------------------------------------
    "雷恩隊長轉身踢開旁邊的物資補給箱，將幾套漆黑厚重的密封式戰鬥裝甲扔在地上。"
    
    aurora_captain "A.D.A.M. 在 B2 和 B3 走廊灌滿了高濃度的生化神經毒氣。凡是不穿防護服進去的人，三十秒內肺部就會化成血水！"
    aurora_captain "立刻把這套【tactical_hazmat_armor 戰術服】給我穿上！內建的高效過濾呼吸閥能幫你們抵擋毒氣，凱夫拉複合裝甲還能擋住普通感染者的撕咬！"
    
    show lengyue at center with dissolve
    lengyue "（迅速撿起一套戰術服俐落套上，回頭冷聲喝令新人們）不想死的就立刻把防護服穿上，把每一處密封閥門扣死！"
    hide lengyue with dissolve
    
    python:
        add_item("tactical_hazmat_armor", 1)
        
    show tactical_hazmat_armor at item_show_center with dissolve
    "【獲得戰術裝備：【tactical_hazmat_armor 戰術服】已放入背包！】"
    "（提供 DEF +30、HP +100，並賦予【毒氣免疫】特殊標籤）"
    "顧臨淵、項天、蘇曉等人立刻照著冷月的動作，迅速將防護服穿戴整齊並扣緊過濾面罩。"
    hide tactical_hazmat_armor with dissolve
    
    lengyue "保護光幕倒數只剩最後 30 秒了。雷恩隊長，你們規劃的第一推進目標是什麼？"
    
    aurora_captain "我們必須一層層殺下去！在 B1 突破防爆大門 ➔ 穿過 B2 毒氣區 ➔ 關閉身後的防爆大門阻擋屍潮 ➔ 最後殺入深層核心主機房，強制重啟或下載 A.D.A.M.！"
    
    # -------------------------------------------------------------
    # 5. 倒數歸零，光幕碎裂與趙虎違規死亡
    # -------------------------------------------------------------
    "【輪迴終端播報】："
    "「倒數結束：00分00秒。新手保護光幕已解除！主線任務啟動：【深入極光地下設施，處置 A.D.A.M. 核心】！」"
    
    "卡嚓————！！"
    "伴隨著金色光幕如玻璃般寸寸碎裂，外圍走廊瞬間響起令人毛骨悚然的喪屍尖嘯與沉重的鐵門拍打聲！"
    
    zhao_hu "什麼狗屁支援部隊！老子在外面是幫會堂主，少拿這種科幻電影威脅我！這破工廠大門都沒鎖，老子現在就要走人！"
    
    # 💀 死亡事件 1：趙虎 (刺青流氓) 撞開生物防禦閥門死亡
    "趙虎無視雷恩隊長與冷月的厲聲警告，猛地衝向旁邊印有『極光重工 · 警告 生物危害 4 級』的密封金屬閥門，一腳猛力踹了上去！"
    
    python:
        if renpy.loadable("audio/laser.ogg"):
            renpy.sound.play("audio/laser.ogg")
            
    "【極光重工 · 超音波生物安全防禦系統啟動】"
    "嗡——————！！"
    "空氣中瞬間爆發出刺耳的高頻音嘯與幽藍色的微波光束！"
    "趙虎連一聲慘叫都未能發出，整個人在兩秒之內被狂暴的奈米超音波震盪解構成了一灘透明黏液！"
    
    zhou_yang "啊啊啊啊——！！死人了！他……他直接化掉了！"
    qian_fugui "這……這真的是人間地獄啊！"
    xiangtian "冷靜點！那門上有高頻殺傷防禦裝置，別亂動！"
    
    lengyue "第一個白痴死了。不想變成黏液的話，就閉上嘴跟緊我。"
    
    aurora_captain "這就是違抗安保條例的下場！這是地下生化研發中心的戰術俯瞰全息藍圖！前方有三道主要封鎖區，選擇你們的第一個突入節點！"
    
    # 🗺️ 點擊式戰術地圖（第一階段：防爆大門）
    call screen stage_1_1_tactical_map_screen(current_step=1)
    
    # -------------------------------------------------------------
    # ⚔️ 6. 【第一波戰鬥】：基礎近戰與陣型教學 (死亡事件 2)
    # -------------------------------------------------------------
    scene bg_aurora_corridor with fade
    show agile_zombie at item_show_center with dissolve
    "轟隆！前方生化隔離防爆大門破裂，三隻肌肉外露、眼眶淌血的敏捷型喪屍怪叫著爬了出來！"
    
    zhou_yang "怪……怪物啊！！別過來！救命啊！"
    "青年周揚嚇得魂飛魄散，失去理智般掉頭就跑，脫離了前排的保護陣型！"
    
    "呼嘯的腥風閃過，一隻敏捷型喪屍自天花板陰影中俯衝撲下，瞬間咬斷了周揚的喉管！"
    
    hide agile_zombie with dissolve
    aurora_captain "蠢貨！離開前排防禦陣型就是這個下場！全體進入戰鬥姿態！"
    xiangtian "前排交給我跟顧兄！蘇曉退到後排保護好自己！"
    suxiao "好……大家小心！"
    
    # 彈出戰前 6 人陣型與前後排配置介面
    call screen party_deployment_screen
    
    python:
        # 初始化第一波戰鬥 (3 隻敏捷型喪屍，自 monsters_db.json 即時讀取數據與頭像)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave1 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'zombie',
            'enemies': [
                create_battle_enemy("agile_zombie", "A", status="嗜血狂暴"),
                create_battle_enemy("agile_zombie", "B", status="嗜血狂暴"),
                create_battle_enemy("agile_zombie", "C", status="敏捷突進")
            ],
            'logs': [
                "⚠️ 【第一波遭遇戰】3 隻敏捷型喪屍發動突襲！",
                "💡 提示：點選左側我方隊員，使用【普通攻擊】或【專屬戰技】消滅前方威脅！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave1)
    
    "【第一波戰鬥結束！三隻敏捷型喪屍被全數擊斃！】"
    
    aurora_captain "防爆大門已突破！打開戰術藍圖，確認下一個前進節點！"
    
    # 🗺️ 點擊式戰術地圖（第二階段：電梯井與毒氣走廊）
    call screen stage_1_1_tactical_map_screen(current_step=2)
    
    # -------------------------------------------------------------
    # 💣 4. 【第二波戰鬥】：毒氣走廊環境 + 手雷教學 (死亡事件 3)
    # -------------------------------------------------------------
    scene bg_aurora_corridor with flash
    
    "眾人跟隨清理隊穿過破裂的氣閘，衝進狹長的地下主通風走廊。"
    "嗤——！！"
    "走廊兩側的黃色管道突然爆裂，滾滾生化濃煙與刺鼻的酸性毒氣迅速瀰漫開來！"
    
    "【警報：高濃度生化毒氣洩漏！每回合扣除 5%% HP，未裝備防毒裝備的目標將持續受創！】"
    
    aurora_captain "前方出現密集怪群堵住了安全門！接住這個『high_explosive 高爆破片手雷』，直接炸平牠們！"
    
    python:
        # 發放 high_explosive 高爆破片手雷物資至背包
        add_item("high_explosive", 2)
        add_item("item_grenade", 2)
        
    show high_explosive at item_show_center with dissolve
    "【獲得戰術物資：【high_explosive 高爆破片手雷】x2 已發放至背包！】"
    "（在戰鬥中點選『物品』欄位使用，可對敵方全體造成 90 點毀滅性範圍傷害）"
    hide high_explosive with dissolve
    
    python:
        # 初始化第二波戰鬥 (5 隻密集怪群 + 毒氣環境，自 monsters_db.json 即時讀取數據與頭像)
        deployed_team = build_deployed_battle_team() if 'build_deployed_battle_team' in globals() else get_team_roster()
        for m in deployed_team:
            m['has_acted'] = False
            
        b_wave2 = {
            'round_number': 1,
            'player_team': deployed_team,
            'world_id': 'zombie',
            'enemies': [
                create_battle_enemy("MOB_ZOMBIE_01", "A", status="毒素附著"),
                create_battle_enemy("MOB_ZOMBIE_01", "B", status="毒素附著"),
                create_battle_enemy("MOB_ZOMBIE_01", "C", status="毒素附著"),
                create_battle_enemy("agile_zombie", "D", status="致命撲咬"),
                create_battle_enemy("agile_zombie", "E", status="嗜血突襲")
            ],
            'logs': [
                "☣️ 【第二波決戰】毒氣環境降臨！高濃度毒氣正侵蝕防護不足的隊員！",
                "💣 戰術提示：點選物品欄使用【high_explosive 高爆破片手雷】迅速瓦解密集怪群！"
            ],
            'current_turn_name': '第 1 回合 · 我方行動階段',
            'is_player_turn': True,
            'selected_actor': None,
            'target_mode': None,
            'selected_skill': None
        }
        
    call screen battle_screen(b_wave2)
    
    "【第二波戰鬥結束！伴隨著手雷的劇烈衝擊波，走廊上的變異腐屍與敏捷型喪屍群被徹底撕碎！】"
    
    # -------------------------------------------------------------
    # 💀 死亡事件 3：錢富貴 (慢吞吞大叔) 動作遲緩被安全門阻隔
    # -------------------------------------------------------------
    "滴——滴——滴——！"
    "【最高生化警報：地下隔離安全防爆閘門即將於 5 秒內永久封閉！】"
    
    lengyue "快衝過去！門要砸下來了！"
    xiangtian "抓緊我！快跑！"
    
    "你、冷月、項天與蘇曉拼盡全力向前飛撲，險之又險地滾過了隔離閥門！"
    "然而，體能匱乏、腿腳發軟的錢富貴大叔落在了最後面……"
    
    qian_fugui "等等我！不要關門啊！我的腿動不了了……救命啊——！"
    
    "轟隆隆————！！"
    "數十噸重的精鋼防爆閘門重重砸落在地，將走廊徹底隔絕！"
    "厚重的鋼門背後，傳來錢富貴絕望的捶打聲與高壓焚化毒氣噴射的淒厲慘叫，幾秒鐘後，聲音徹底歸於死寂……"
    
    lengyue "趙虎、周揚、錢富貴……6 個新人死了 3 個。現在算上你，只剩下你們 3 個新人了。"
    lengyue "防爆門徹底落下，後路已斷。打開戰術藍圖，直搗最深處的生物神經主機！"
    
    # 🗺️ 點擊式戰術地圖（第三階段：神經核心機房）
    call screen stage_1_1_tactical_map_screen(current_step=3)
    
    # -------------------------------------------------------------
    # 🧠 5. 底層生物神經網絡 A.D.A.M. 與智者分支檢定
    # -------------------------------------------------------------
    scene bg_aurora_core with fade
    
    "穿過隔離防爆門後，殘存的隊員（顧臨淵、冷月、項天、蘇曉）踏入了極光重工最核心的地下設施。"
    "巨大透明圓柱容器中浸泡著無數閃爍著微光的生物腦神經組織，藍色的全息代碼流如瀑布般在空中流淌。"
    
    adam_ai "警告……未知生物入侵核心協議……A.D.A.M. 亞當神經元矩陣正在執行資料自毀……"
    
    # 計算隊伍中最高智力 (INT)
    python:
        team_roster = get_team_roster()
        team_max_int = max([int(m.get('int', 20)) for m in team_roster])
        has_int_talent = (team_max_int >= 100)
        
    if has_int_talent:
        n "【智者思維感知】隊伍最高智力達到 [team_max_int] 點（達標 >= 100，蘇曉的敏銳智力感知起了作用），你捕捉到了主機中隱藏的神經架構原始碼！"
        menu:
            "【🧠 智者檢定】發動思維入侵，剝離並下載 A.D.A.M. 神經核心原始碼":
                python:
                    add_item("ITEM_HIVE_AI_BACKUP", 1)
                    points += 1500
                    add_fate_shard("C", 1)
                
                show adamcore at item_show_center with dissolve
                "【智者判定成功！】你以強大的智力算力強行突破了自毀防火牆，成功將【亞當神經元矩陣備份 (A.D.A.M. Core)】下載至戰術終端！"
                "（此核心數據可帶回個人房間，解鎖 3D 列印高科技裝備終端與基因鎖藥劑研發！）"
                hide adamcore with dissolve
                "獲得額外獎勵：生存點數 +1,500 點、C 階命運碎片 x1！"
                
            "遵從極光重工清理隊長命令，直接引爆神經網絡主機":
                python:
                    points += 800
                "伴隨著定向炸藥的轟鳴，A.D.A.M. 核心化為漫天火海，極光重工的生化罪證被徹底抹除。"
                "獲得基礎任務獎勵：生存點數 +800 點。"
    else:
        n "隊伍當前最高智力為 [team_max_int] 點（未達門檻 100 點），無法承受高維神經網絡的反噬，只能由清理隊安保隊長安置炸藥將主機引爆。"
        python:
            points += 800
        "伴隨著烈焰升騰，A.D.A.M. 核心被徹底摧毀。獲得基礎任務獎勵：生存點數 +800 點。"

    # -------------------------------------------------------------
    # 🏆 6. 副本結算與回歸輪迴廣場
    # -------------------------------------------------------------
    scene bg_aurora_core with flash
    
    "當主機被徹底處置完畢時，手錶上的倒數歸零，虛空中投射下一道神聖而冰冷的純白光柱！"
    
    python:
        # 新人存活結算：存活 2 名新人 (項天與蘇曉)
        rookie_bonus = 2000
        points += rookie_bonus
        add_fate_shard("D", 2)
        global current_main_stage_index
        current_main_stage_index = max(current_main_stage_index if 'current_main_stage_index' in globals() else 1, 2)
        if 'reset_teammate_chat_quota' in globals():
            reset_teammate_chat_quota()
        if renpy.loadable("audio/levelup.ogg"):
            renpy.sound.play("audio/levelup.ogg")
            
    z "【主線任務 · 喪屍末日世界（極光重工遺址）已完成！】"
    z "結算統計：成功保護 2 名新人【項天】與【蘇曉】存活回歸（額外獲得生存點數 +2,000 點、D 階命運碎片 x2）！"
    z "目前持有總點數：[points] 點。"
    
    xiangtian "呼……總算挺過來了。顧臨淵、冷月，多虧有你們的配合！"
    suxiao "我們……真的活下來了！這一切簡直像做夢一樣……"
    lengyue "別高興得太早。這只是輪迴空間的第一道篩選，真正的地獄才剛剛開始。"
    
    scene bg_main_room_topdown with fade
    
    "伴隨著聖光籠罩，四道身影自純白光柱中緩緩降落在輪迴空間大廳的中央石碑前……"
    "溫暖純淨的修復光芒洗滌了全身的疲憊與血腥，四周再次變成了無垠浩瀚的白玉殿堂——輪迴空間中央廣場。"
    
    show lengyue at center with dissolve
    lengyue "站穩了。恭喜你們三個活過了第一場篩選，現在你們才算真正成為『輪迴者』。"
    
    xiangtian "這裡……就是所謂的輪迴空間？天空中漂浮著的那顆巨大光球是什麼？"
    
    lengyue "那是『輪迴核心』，也是主宰整個空間與所有位面任務的樞紐。"
    lengyue "趁下一場恐怖片降臨之前，我先跟你們說明這裡的鐵律，記不住的人下一場就只會變成屍體。"
    
    lengyue "【第一，生存與抹殺規則】。"
    lengyue "每完成一場任務，我們會有 10 天的休息整備期。時間一到，輪迴空間會強制將我們傳送進下一個世界。"
    lengyue "手錶上的主線任務是絕對指令，未完成或點數為負者，將被輪迴核心直接『抹殺』。"
    
    lengyue "【第二，個人專屬房間與家園】。"
    lengyue "廣場四周排列著無數扇空白的金屬門。只要走上前，用意識握住門把手，那扇門就會綁定成為你的『私人房間』。"
    lengyue "在你的房間裡，你可以依照大腦想像隨意具現環境——無論是陽光沙灘、豪華別墅、重力修煉室，甚至科研實驗室。"
    lengyue "而且我們在副本中搶到的高科技設備（例如剛才拿到的 A.D.A.M. 核心），都可以安裝在房間裡解鎖 3D 裝備打印機與設施升級。"
    
    suxiao "可以依照自己的想像創造房間……也就是說，我終於能有一個安靜看書寫作的地方了？"
    xiangtian "這簡直就是維度級的造物能力……那最關鍵的戰力強化呢？"
    
    lengyue "這就是【第三，兌換與血統強化體系】。"
    lengyue "走向中央光球或旁邊的石碑，用意識連結，就能開啟龐大的兌換商城。"
    lengyue "在這裡，剛才結算獲得的【生存點數】與【命運碎片（D/C/B/A/S 級）】是唯一的硬通貨。"
    lengyue "商城裡包含無數種體系：高科技槍械裝甲、奈米急救物資、武道內力真氣、修真修仙功法、西方吸血鬼與狼人變異，甚至是基因鎖解鎖藥劑與精神念力。"
    lengyue "記住，點數和碎片極度珍貴，千萬不要盲目亂換。一個成熟的團隊必須有前排坦克、遠程輸出、精神感知與後勤輔助。"
    
    hide lengyue with dissolve
    
    xiangtian "明白了。我們現在有生存點數與 D 階碎片，必須先好好規劃強化方向。"
    suxiao "顧臨淵隊長，我們先去中央光球和石碑那邊看看吧！"
    
    "冷月的話音落下，石碑與中央光球閃爍起柔和的導航光芒，等待著你們進行血統強化與物資整備。"
    
    jump main_room_exploration