########################################################
## This file contains the three tabs found on the
## Settings screen. It's organized as follows:
##   screen settings_tabs
##   screen profile_pic
##     screen input_popup
##   screen other_settings
##     label restart_game
##   screen preferences
##     screen voice_buttons
##     screen ringtone_drowdown
########################################################

init python:

    ## This lets you change the MC's profile picture by clicking on it
    ## Currently you can only use the pre-set images, not upload your own
    def MC_pic_change():   
        if persistent.MC_pic == 5:
            persistent.MC_pic = 1
        else:
            persistent.MC_pic += 1
            
        global m
        thepic = 'Profile Pics/MC/MC-[persistent.MC_pic].png'
        m.prof_pic = thepic
        renpy.retain_after_load()
    
default email_tone_dict = { 'Default 1': 'sfx/Ringtones etc/email_basic_1.wav', 
                            'Default 2': 'sfx/Ringtones etc/email_basic_2.wav',     
                            'Default 3': 'sfx/Ringtones etc/email_basic_3.wav'
                          }
                          
default text_tone_dict = {  'Default': 'sfx/Ringtones etc/text_basic_1.wav', 
                            'Jumin Han': 'sfx/Ringtones etc/text_basic_ju.wav',     
                            'Jaehee Kang': 'sfx/Ringtones etc/text_basic_ja.wav',
                            '707': 'sfx/Ringtones etc/text_basic_s.wav',
                            'Yoosung★': 'sfx/Ringtones etc/text_basic_y.wav',
                            'ZEN': 'sfx/Ringtones etc/text_basic_z.wav'
                         }
                            
default ringtone_dict = {   'Default': 'sfx/Ringtones etc/phone_basic_1.wav', 
                            'Jumin Han': 'sfx/Ringtones etc/phone_basic_ju.wav',     
                            'Jaehee Kang': 'sfx/Ringtones etc/phone_basic_ja.wav',
                            '707': 'sfx/Ringtones etc/phone_basic_s.wav',
                            'Yoosung★': 'sfx/Ringtones etc/phone_basic_y.wav',
                            'ZEN': 'sfx/Ringtones etc/phone_basic_z.wav'
                        }
                        
# This is organized as a list of lists. The first item is the name of
# the category. The second item is a list of the names of the tones
# as you defined them above in the dictionary. To define more categories,
# put a comma after the second-last bracket and define another list like
# shown below
default email_tone_list = [ ["Basic", ['Default 1', 'Default 2', 'Default 3' ]]
                          ]
                          
default text_tone_list = [ ["Basic", ['Default', 'Jumin Han', 'Jaehee Kang', '707', 
                                     'Yoosung★', 'ZEN' ]]
                          ]
                          
default ringtone_list = [ ["Basic", ['Default', 'Jumin Han', 'Jaehee Kang', '707', 
                                     'Yoosung★', 'ZEN' ]]
                          ]
                          
default persistent.phone_tone = 'sfx/Ringtones etc/phone_basic_1.wav'
default persistent.text_tone = "sfx/Ringtones etc/text_basic_1.wav"
default persistent.email_tone = 'sfx/Ringtones etc/email_basic_1.wav'
default persistent.phone_tone_name = "Default"
default persistent.text_tone_name = "Default"
default persistent.email_tone_name = "Default 1"


########################################################
## The three tabs on the Settings screen
########################################################

screen settings_tabs(active_tab):

    # "Backgrounds" of the different panels
    window:
        xalign 0.5
        yalign 0.14
        maximum(700,70)
        has hbox
        spacing 10
        # Account / Sound / Others tab
        textbutton _('Profile'):
            text_style "settings_tabs" 
            xsize 231
            ysize 57
            if active_tab == "Profile":
                background "menu_tab_active"
            else:
                background "menu_tab_inactive"
                hover_background "menu_tab_inactive_hover"
                action Show("profile_pic", Dissolve(0.5))
                activate_sound 'sfx/UI/settings_tab_switch.mp3'
                
        textbutton _('Sound'):
            text_style "settings_tabs" 
            xsize 231
            ysize 57
            if active_tab == "Sound":
                background "menu_tab_active"
            else:
                background "menu_tab_inactive"
                hover_background "menu_tab_inactive_hover"
                action Show("preferences", Dissolve(0.5))
                activate_sound 'sfx/UI/settings_tab_switch.mp3'
            
        textbutton _('Others'):
            text_style "settings_tabs"  
            xsize 231
            ysize 57
            if active_tab == "Others":
                background "menu_tab_active"
            else:
                background "menu_tab_inactive"
                hover_background "menu_tab_inactive_hover"
                action Show("other_settings", Dissolve(0.5))  
                activate_sound 'sfx/UI/settings_tab_switch.mp3'                
                

        
########################################################
## The "Profile" tab of Settings. Allows you to change
## your profile pic, name, and preferred pronouns
########################################################

screen profile_pic:
    
    tag settings_screen
    modal True

    use starry_night

    if not persistent.first_boot:
        use settings_tabs("Profile")  
    
    window:
        yalign 0.7
        xalign 0.05
        maximum(325, 900)
        # Edit MC's Name
        add "name_line" xalign 0.079 yalign 0.475        
        text persistent.name style "my_name"
        
        imagebutton:
            idle "menu_edit"
            focus_mask None
            xalign 0.06
            yalign 0.453
            hover Transform("Phone UI/Main Menu/menu_pencil_long.png", zoom=1.03)
            action Show('input_popup', prompt='Please input a name.') 

        # MC's profile picture
        imagebutton:
            idle "MC_profpic"
            xalign 0.055
            action [Function(MC_pic_change), renpy.restart_interaction]
            focus_mask True
      
    # Pick your pronouns
    window:
        style "pronoun_window"
        
        has vbox
        spacing 15
        xalign 0.5
        yalign 0.5
        text "Preferred Pronouns" style "pronoun_label"
        button:     
            action [SetField(persistent, "pronoun", "female"), set_pronouns, renpy.restart_interaction]
            has hbox
            spacing 10
            if persistent.pronoun == "female":
                add "radio_on"
                text 'she/her' color '#fff' hover_color '#ddd'
            else:
                add "radio_off"            
                text 'she/her' hover_color '#fff' color '#ddd'
            
        button:
            action [SetField(persistent, "pronoun", "male"), set_pronouns, renpy.restart_interaction]
            has hbox
            spacing 10
            if persistent.pronoun == "male":
                add "radio_on"
                text 'he/him' color '#fff' hover_color '#ddd'
            else:
                add "radio_off"
                text 'he/him' hover_color '#fff' color '#ddd'
            
            
        button:
            action [SetField(persistent, "pronoun", "non binary"), set_pronouns, renpy.restart_interaction]
            has hbox
            spacing 10
            if persistent.pronoun == "non binary":
                add "radio_on"
                text 'they/them' color '#fff' hover_color '#ddd'
            else:
                add "radio_off"
                text 'they/them' hover_color '#fff' color '#ddd'
             
        
        
    if not persistent.first_boot:
        use menu_header("Settings", Hide('profile_pic', Dissolve(0.5)))
    else:
        use menu_header("Customize your Profile", MainMenu(False))
        
    if not persistent.first_boot:            
        # Save / Load
        imagebutton:
            yalign 0.978
            xalign 0.66
            idle "save_btn"
            hover im.FactorScale("Phone UI/Main Menu/menu_save_btn.png",1.1)
            action Show("save", Dissolve(0.5))
            
        imagebutton:
            yalign 0.978
            xalign 0.974
            idle "load_btn"
            hover im.FactorScale("Phone UI/Main Menu/menu_load_btn.png",1.1)
            action Show("load", Dissolve(0.5))
        
        
        # Possibly temporary, but shows how many heart points you've earned
        # with each character
        
        grid 4 4:
            xalign 0.5
            yalign 0.95
            add 'greet jaehee'
            add 'greet jumin'
            add 'greet ray'
            add 'greet rika'
            
            text str(ja.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(ju.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(sa.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(ri.heart_points) + " {image=header_heart}" style "point_indicator"
            
            add 'greet seven'
            add 'greet v'
            add 'greet yoosung'
            add 'greet zen'
            
            text str(s.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(v.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(y.heart_points) + " {image=header_heart}" style "point_indicator"
            text str(z.heart_points) + " {image=header_heart}" style "point_indicator" 
    

########################################################
## The Input Prompt to get text from the user
########################################################
                
screen input_popup(prompt=''):

    zorder 100
    modal True
    
    $ old_name = persistent.name    # We save this so we can reset it if they don't want to change it
    $ input = Input(value=MyInputValue("persistent.name", persistent.name), style="my_input", length=20)
    
    window:
        maximum(550,313)
        background 'input_popup_bkgr'
        xalign 0.5
        yalign 0.4
        imagebutton:
            align (1.0, 0.0)
            idle 'input_close'
            hover 'input_close_hover'
            action [SetField(m, 'name', old_name), 
                    SetVariable('name', old_name), SetField(persistent, 'name', old_name), 
                    renpy.retain_after_load, Hide('input_popup')]
        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            text prompt color '#fff' xalign 0.5 text_align 0.5
            fixed:
                xsize 500 
                ysize 75
                xalign 0.5
                add 'input_square'
                add input  xalign 0.5 yalign 0.5
            textbutton _('Confirm'):
                text_style 'mode_select'
                xalign 0.5
                xsize 240
                ysize 80
                background 'menu_select_btn' padding(20,20)
                hover_background 'menu_select_btn_hover'
                action [Hide('input_popup')]


########################################################
## The "Others" tab of the settings screen
## Includes VN options and Ringtone selection
########################################################
              
screen other_settings():

    tag settings_screen
    modal True

    #add "Phone UI/Main Menu/menu_settings_bg.png"
    use starry_night
    use menu_header("Settings", Hide('other_settings', Dissolve(0.5)))
    use settings_tabs("Others")
        
    window:
        maximum(700, 800)
        xalign 0.5
        yalign 0.5
        has vbox
        spacing 30
            
        window:
            maximum(675,350)
            add "menu_settings_panel"
            text "Other Settings" style "settings_style" xpos 55 ypos 5
            
            hbox:
                align (0.2, 0.5)
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time") bar_invert True
                    
                    null height 10
                    hbox:
                        window:
                            xysize (25,25)
                            background "#515151"
                            yalign 0.5
                            if persistent.custom_footers:
                                add Transform("Phone UI/Main Menu/main02_tick.png", zoom=0.65) align (0.0,1.0) yoffset -5
                            
                        textbutton _("Custom Chat Footers"):
                            align (0.5, 1.0)
                            action ToggleField(persistent, "custom_footers")
            
        window:
            maximum(675,250)
            add "menu_settings_panel"
            text "VN Settings" style "settings_style" xpos 55 ypos 5

            vbox:
                xalign 0.2
                yalign 0.75
                style_prefix "check"
                label _("Skip")
                textbutton _("Unseen Text") action Preference("skip", "toggle")
                textbutton _("After Choices") action Preference("after choices", "toggle")
                textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))
                
        window:
            xysize (675,180)
            background "menu_settings_panel"
            text "Variables for testing" style "settings_style" xpos 55 ypos 5

            window:
                xysize (660, 120)
                yoffset 50
                align (0.5, 0.0)
                has hbox
                xysize (660, 120)
                align (0.5, 0.0)
                spacing 10
                hbox:
                    xalign 0.2
                    yalign 0.5
                    spacing 10
                    window:
                        xysize (25,25)
                        yalign 0.5
                        background "#515151"
                        if persistent.testing_mode:
                            add Transform("Phone UI/Main Menu/main02_tick.png", zoom=0.65) align (0.0,1.0) yoffset -5
                        
                    textbutton _("Testing Mode"):
                        align (0.5, 1.0)
                        action ToggleField(persistent, "testing_mode")
                        
                hbox:
                    xalign 0.2
                    yalign 0.5
                    spacing 10
                    window:
                        xysize (25,25)
                        yalign 0.5
                        background "#515151"
                        if persistent.real_time:
                            add Transform("Phone UI/Main Menu/main02_tick.png", zoom=0.65) align (0.0,1.0) yoffset -5
                        
                    textbutton _("Real-Time Mode"):
                        align (0.5, 1.0)
                        action ToggleField(persistent, "real_time")
                        
            hbox:
                xalign 0.2
                yalign 0.5
                spacing 10
                yoffset 90
                xoffset -65
                window:
                    xysize (25,25)
                    yalign 0.5
                    background "#515151"
                    if hacked_effect:
                        add Transform("Phone UI/Main Menu/main02_tick.png", zoom=0.65) align (0.0,1.0) yoffset -5
                    
                textbutton _("Hacked Effect"):
                    align (0.5, 1.0)
                    action ToggleVariable('hacked_effect')
                
            # Additional vboxes of type "radio_pref" or "check_pref" can be
            # added here, to add additional creator-defined preferences.
            
        
        
        window:
            maximum (520, 130)
            xalign 0.5
            has hbox
            spacing 40
            textbutton _('Go to Mode Select'):
                text_style 'mode_select'
                xsize 240
                ysize 120
                background 'menu_select_btn' padding(20,20)
                hover_background 'menu_select_btn_hover'
                action [ToggleVariable("greeted", False, False), renpy.full_restart]
                
            textbutton _('Start Over'):
                text_style 'mode_select'
                xsize 240
                ysize 120
                background 'menu_select_btn' padding(20,20)
                hover_background 'menu_select_btn_hover'
                action Show("confirm", message="Are you sure you want to start over? You'll be unable to return to this point except through a save file.", 
                        yes_action=[Hide('confirm'), Jump("restart_game")], no_action=Hide('confirm'))
            
            
# *********************************
# Restart Game -- resets variables
# *********************************       
label restart_game:
    python:
        # removes heart points from all the characters
        for person in character_list:
            person.reset_heart()
        
        # presumably some more resets here as needed
        persistent.on_route = False
        renpy.full_restart()
        



## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##

screen preferences():

    tag settings_screen
    modal True

    use starry_night
    use menu_header("Settings", Hide('preferences', Dissolve(0.5)))
    use settings_tabs("Sound")
    
    viewport:
        xysize(700, 1070)
        xalign 0.5
        yalign 0.95
        draggable True
        mousewheel True
        scrollbars "vertical"
        side_spacing 5
        has vbox
        spacing 30
        xalign 0.5
        
        
  
        window:
            maximum(675,480)
            background "menu_settings_panel" padding(10,10)
            xalign 0.5
            has vbox
            spacing 30
            xalign 0.5
            yalign 0.34
            text "Sound" style "settings_style" xpos 55 ypos -5
            
            vbox:      
                spacing 15
                xsize 625
                hbox:
                    spacing 30
                    xsize 520
                    textbutton _("BGM"):
                        background "menu_sound_sfx"
                        text_style "sound_tags"
                        xsize 163
                        ysize 50
                        action ToggleMute("music")
                    bar value Preference("music volume") ypos 15 thumb_offset 18 left_gutter 18
                hbox:
                    spacing 30
                    xsize 520
                    textbutton _("SFX"):
                        background "menu_sound_sfx"
                        text_style "sound_tags"
                        xsize 163
                        ysize 50
                        action ToggleMute("sfx")
                    bar value Preference("sound volume") ypos 15 thumb_offset 18
                    if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)
                hbox:
                    spacing 30
                    xsize 520
                    textbutton _("Voice"):
                        background "menu_sound_sfx"
                        text_style "sound_tags"
                        xsize 163
                        ysize 50
                        action ToggleMute("voice")
                    bar value Preference("voice volume") ypos 15 thumb_offset 18
                    if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)
                hbox:
                    spacing 30
                    xsize 520
                    textbutton _("Voice SFX"):
                        background "menu_sound_sfx"
                        text_style "sound_tags"
                        xsize 163
                        ysize 50
                        action ToggleMute("voice_sfx")
                    bar value set_voicesfx_volume() ypos 15 thumb_offset 18
                    if sample_voice_sfx:
                                textbutton _("Test") action Play("voice_sfx", sample_voice_sfx)
                    
                textbutton _("Mute All"):
                    action Preference("all mute", "toggle")
                    style "mute_all_button" xalign 0.45
            
        window:
            maximum(675,620)
            background "menu_settings_panel" padding(10,10)
            has vbox
            xalign 0.5
            yalign 0.5
            spacing 15
            text "Voice" style "settings_style" xpos 185 ypos -5
            
            ## There are few voiced lines in this program, so currently
            ## the effects of these buttons will not be very noticeable
            hbox:
                xalign 0.5
                yalign 0.5
                spacing -35
                null width 165            
                grid 2 5:                
                    transpose True
                    spacing 30
                    align (0.5, 0.0)
                    
                    text "Jumin Han" style "settings_style"
                    text "ZEN" style "settings_style"
                    text "707" style "settings_style"
                    text "Ray" style "settings_style"
                    text "Others" style "settings_style"
                    
                    use voice_buttons('jumin')
                    use voice_buttons('zen')
                    use voice_buttons('seven')
                    use voice_buttons('saeran')
                    use voice_buttons('other')
                    
                
                grid 2 4:
                    spacing 30
                    transpose True
                    align (0.5, 0.0)
                    text "Yoosung★" style "settings_style"
                    text "Jaehee Kang" style "settings_style"
                    text "V" style "settings_style"
                    text "Rika" style "settings_style"
                    
                    use voice_buttons('yoosung')
                    use voice_buttons('jaehee')
                    use voice_buttons('v')
                    use voice_buttons('rika')
                    
                    
        window:
            maximum(675,360)
            background "menu_settings_panel"
            align (0.5, 0.34)
            text "Ringtone" style "settings_style" xpos 55 ypos 5
            window:
                align (0.5, 0.85)
                xysize (640, 300)
                has vbox
                align (0.5, 0.5)
                spacing 12
                button:
                    xysize (300, 80)
                    background 'menu_ringtone_box'
                    hover_foreground 'menu_ringtone_box'
                    vbox:
                        align (0.5, 0.5)
                        text "Text Sound" style 'ringtone_change'
                        text persistent.text_tone_name style 'ringtone_description'
                    action Show('ringtone_dropdown', title='Text Sound', tone='text')
                
                button:
                    xysize (300, 80)
                    background 'menu_ringtone_box'
                    hover_foreground 'menu_ringtone_box'
                    vbox:
                        align (0.5, 0.5)
                        text "Email Sound" style 'ringtone_change'
                        text persistent.email_tone_name style 'ringtone_description'
                    action Show('ringtone_dropdown', title='Email Sound', tone='text')
                    
                button:
                    xysize (300, 80)
                    background 'menu_ringtone_box'
                    hover_foreground 'menu_ringtone_box'
                    vbox:
                        align (0.5, 0.5)
                        text "Ringtone" style 'ringtone_change'
                        text persistent.phone_tone_name style 'ringtone_description'
                    action Show('ringtone_dropdown', title='Ringtone', tone='text')

## A helper screen to display the buttons for toggling
## each characters' voice on or off
screen voice_buttons(voice_char):

    $ voice_char = voice_char + '_voice'
    
    button:
        xysize (120, 30)
        idle_child Text("On", style="voice_toggle_on")
        hover_child Text("On", style="voice_toggle_on")
        selected_child Text("Off", style="voice_toggle_off")
        action ToggleVoiceMute(voice_char)
        
## A helper screen for displaying the choices you have for
## ringtones, email tones, and text tones
screen ringtone_dropdown(title, tone):

    modal True
    add "Phone UI/choice_dark.png"
    window:
        xysize(675,1000)
        background "menu_settings_panel_bright"
        align (0.5, 0.5)
        
        imagebutton:
            align (1.0, 0.0)
            idle 'input_close'
            hover 'input_close_hover'
            action Hide('ringtone_dropdown')
            
        text title style "settings_style" xpos 55 ypos 5
           
        viewport:
            xysize(600, 940)
            xalign 0.5
            yalign 0.85
            draggable True
            mousewheel True
            scrollbars "vertical"
            side_spacing 5
            has vbox
            xsize 550
            spacing 15
            xalign 0.5
            yalign 0.5
            
            
            # Text message tones
            if title == 'Text Sound':
                $ the_list = text_tone_list
                $ the_dict = text_tone_dict
                $ p_field = 'text_tone'
            elif title == 'Email Sound':
                $ the_list = email_tone_list
                $ the_dict = email_tone_dict
                $ p_field = 'email_tone'
            elif title == 'Ringtone':
                $ the_list = ringtone_list
                $ the_dict = ringtone_dict
                $ p_field = 'phone_tone'
                
            for pair in the_list:
                # Name of the category
                null height 10
                text pair[0] color '#fff' xalign 0.5 text_align 0.5
                null height 10
                
                # List of the ringtones                
                for tone in pair[1]:
                    textbutton _(tone):
                        xysize(450, 60)
                        background '#fff'
                        text_color '#000' 
                        text_xalign 0.5 
                        text_align 0.5 
                        text_yalign 0.5
                        align (0.5, 0.5)
                        text_hover_color "#12736d"
                        selected_background "#d0d0d0"                    
                        selected getattr(persistent, p_field) == the_dict[tone]
                        if title != "Ringtone":
                            activate_sound the_dict[tone]
                            action [SetField(persistent, p_field, the_dict[tone]),
                                    SetField(persistent, p_field + '_name', tone)]
                        else:
                            activate_sound "<from 0 to 2>" + the_dict[tone]
                            action [renpy.music.stop(channel=config.play_channel),
                                    SetField(persistent, p_field, the_dict[tone]),
                                    SetField(persistent, p_field + '_name', tone)]
                    
                    
                    
                    
                    
                    