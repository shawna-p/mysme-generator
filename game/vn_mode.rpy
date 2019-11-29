#************************************
#************************************
#********Visual Novel Mode***********
#************************************
#************************************

#####################################
## Backgrounds
#####################################

image bg mint_eye_room = "VN Mode/Backgrounds/mint_eye_room.png"
image bg rika_apartment = "VN Mode/Backgrounds/rika_apartment.png"
image bg cr_meeting_room = "VN Mode/Backgrounds/cr_meeting_room.png"
image bg good_end = "VN Mode/Backgrounds/good_end.jpg"
image bg normal_end = "VN Mode/Backgrounds/normal_end.jpg"
image bg bad_end = "VN Mode/Backgrounds/bad_end.jpg"
image bg black = '#000000'


#####################################
## Transforms/VN Positions
#####################################

# In order from leftmost to rightmost pose
transform vn_farleft:
    xalign 0.0
    yalign 1.0
    xoffset -300
    yoffset 0
    zoom 1.0

transform vn_left:
    xalign 0.0
    yalign 1.0
    xoffset -100
    zoom 1.0
    
transform vn_midleft:
    xalign 0.0
    yalign 1.0
    xoffset -50
    zoom 1.0
    
transform vn_center:
    xalign 0.5
    yalign 0.5
    zoom 1.15
    yoffset 280
    xoffset 0
    xanchor 0.5
    yanchor 0.5
    
transform vn_midright:
    xalign 1.0
    yalign 1.0
    xoffset 50
    zoom 1.0
    
transform vn_right:
    xalign 1.0
    yalign 1.0
    xoffset 100
    zoom 1.0
    
transform vn_farright:
    xalign 1.0
    yalign 1.0
    yoffset 0
    xoffset 300    
    zoom 1.0
    
    
#####################################
## VN Setup
#####################################

label vn_begin():
    window auto
    $ chatroom_hp = 0
    scene bg black
    stop music
    hide screen starry_night
    hide screen phone_overlay
    hide screen messenger_screen 
    hide screen pause_button
    hide screen chatroom_timeline
    
    # Hide all the popup screens
    hide screen text_msg_popup
    hide screen text_pop_2
    hide screen text_pop_3
    hide screen email_popup
    
    show screen vn_overlay
    $ vn_choice = True
    $ _history_list = [] # This clears the History screen
    $ _history = True
    
    if current_chatroom.vn_obj.played:
        if not persistent.testing_mode:
            $ observing = True
        else:
            pass
    else:
        $ observing = False
    if _in_replay:
        $ observing = True
        $ set_name_pfp()
        $ set_pronouns()
        
    return
        
label vn_end():
    hide screen vn_overlay    
    $ vn_choice = False
    $ renpy.retain_after_load()
    call press_save_and_exit(False) 
    return
        
#####################################
## This screen shows the clock
#####################################

screen vn_overlay():

    hbox:
        add my_menu_clock xalign 0.0 yalign 0.0 xpos 5

        
################################################
## This is the custom history screen
## for VN Mode
## https://www.renpy.org/doc/html/history.html
################################################

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    add '#000b'
    
    # Close button
    button:
        xalign 1.0
        yalign 0.0
        focus_mask True
        add "close_button"
        action Return()        
        text "Close" style "CG_close"
    
    
    viewport:
        yinitial 1.0
        scrollbars "vertical"
        mousewheel True
        draggable True
        side_yfill True

        ysize 1235
        yalign 1.0

        vbox:
            style_prefix "history"
            spacing 20
            null height 5
            for h in _history_list:

                fixed:
                    yfit True

                    if h.who:

                        label h.who + ':':
                            style "history_name"

                            ## Take the color of the who text from the 
                            ## Character, if set.
                            if "color" in h.who_args:
                                text_color h.who_args["color"]

                    $ what = renpy.filter_text_tags(h.what, 
                                    allow=gui.history_allow_tags)
                    text what

            if not _history_list:
                label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = set()


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    text_align gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    text_align gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5
