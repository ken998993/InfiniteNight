# =========================================================
# 角色與變數定義
# =========================================================
define n = Character(None)
define z = Character("神秘聲音")
define m = Character("陌生男人")
define x = Character("系統")

# 定義一個用來顯示玩家狀態的畫面

# =========================================================
# 遊戲開始 (整個專案只能有一個 label start)
# =========================================================
label start:
    $ hp = 100
    $ sanity = 100
    $ points = 0
    $ courage = 0
    if 'team_roster' not in globals() or not team_roster:
        $ team_roster = get_team_roster()

    show screen player_status

    scene trial_room

    n "……"
    n "你醒了過來。"
    n "冰冷的地板貼著你的臉。"
    n "你睜開眼睛。"
    n "這是一個你從未見過的白色房間。"

    pause 1.0

    z "歡迎來到「試煉空間」。"

    menu:
        "「你是誰？」":
            $ courage += 5
            z "我是負責管理試煉的系統。"
            jump introduction

        "保持沉默":
            z "沉默並不能改變你的命運。"
            jump introduction


label introduction:
    z "從現在開始，你將進入一個又一個的試煉世界。"
    z "完成任務，你可以獲得生存點數。"
    
    menu:
        "「我不參加。」":
            jump refuse
        "「我要活下去。」":
            $ courage += 10
            jump accept


label refuse:
    z "拒絕試煉。"
    $ hp = 0
    n "一股劇痛突然從你的胸口傳來，視線逐漸變黑。"
    x "【試煉者死亡。】"
    return


label accept:
    n "你深吸了一口氣，既然已經沒有退路，那就只能活下去。"
    z "很好，第一次試煉即將開始：《喪屍都市》。"
    jump zombieCity


