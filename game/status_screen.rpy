screen player_status():
    frame:
        xalign 0.03
        yalign 0.03
        padding (16, 12)
        background "#000000aa"

        vbox:
            spacing 6
            text f"HP: {hp} / 100" size 18 color "#ffffff"
            
            bar:
                value hp
                range 100
                xmaximum 180
                ymaximum 14
                left_bar "#2ecc71"
                right_bar "#444444"