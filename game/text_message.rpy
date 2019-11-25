

    
########################################################               
## This is the text message hub, where you can click
## on any of your ongoing text conversations
########################################################
screen text_message_hub():

    tag menu
    on 'replace' action FileSave(mm_auto, confirm=False)
    on 'show' action FileSave(mm_auto, confirm=False)
    
    use menu_header('Text Message', Show('chat_home', Dissolve(0.5))):

        viewport:
            xsize 725
            ysize 1150
            draggable True
            mousewheel True

            xalign 0.5
            yalign 0.95
            
            vbox:
                spacing 10
                for i in all_characters:
                    # First we display unread messages
                    if i.text_msg.msg_list and not i.text_msg.read:
                        use text_hub_display(i)
                for i in all_characters:
                    # Now we display read messages
                    if i.text_msg.msg_list and i.text_msg.read:                 
                        use text_hub_display(i)
                
                
screen text_hub_display(i):

    python:
        text_log = i.text_msg.msg_list
        text_read = i.text_msg.read
        text_label = i.text_msg.reply_label
        text_notified = i.text_msg.notified

        if len(text_log) > 0:
            last_text = text_log[-1]
            text_time = last_text.thetime
        else:
            last_text = False
            text_time = False
    

    
    button:              
        if last_text and text_read:                                         
            background 'message_idle_bkgr'
            hover_background 'message_hover_bkgr'
        elif last_text:
            background 'unread_message_idle_bkgr'
            hover_background 'unread_message_hover_bkgr'
        # If there's a label we jump to it, otherwise
        # we just show the messages
        if text_label and i.real_time_text:
            action [SetVariable('CG_who', i),
                    Function(i.text_msg.mark_read),
                    Jump(text_label)]
        else:
            action [SetVariable('CG_who', i),
                    Function(i.text_msg.mark_read),
                    Show('text_message_screen', sender=i)]
            

        activate_sound 'audio/sfx/UI/email_next_arrow.mp3'        
        ysize 150
        xsize 725

        hbox:
            align (0.5, 0.5)
            spacing 10                                
            window:
                xysize (135, 135)
                align (0.0, 0.5)
                add Transform(last_text.who.prof_pic, size=(127,127)):
                    align(0.5, 0.5)
            
            window:
                xysize(320,135)
                yalign 0.5
                has vbox
                align (0.0, 0.5)
                text last_text.who.name style "save_slot_text"
                spacing 40     
                text text_popup_preview(last_text, 16):
                    style "save_slot_text"
                
            window:
                xmaximum 230
                has vbox
                align (0.5, 0.5)
                if last_text and text_read:
                    spacing 50
                else:
                    spacing 30
                text (text_time.day + '/' + text_time.month_num 
                        + '/' + text_time.year + ' ' 
                        + text_time.twelve_hour + ':' 
                        + text_time.minute + text_time.am_pm):
                            style "save_timestamp"
                if last_text and text_read:
                    add 'read_text_envelope' xalign 1.0
                else:
                    hbox:
                        spacing 10
                        xalign 1.0
                        add 'new_text'
                        add 'new_text_envelope'
                    
    
                                            
########################################################               
## This screen takes care of the popups that notify
## the user when there is a new text message   
########################################################            
screen text_msg_popup(c):

    #modal True
    zorder 100
    

    if len(c.text_msg.msg_list) > 0:
        $ last_msg = c.text_msg.msg_list[-1]
    else:
        $ last_msg = False
        
    window:
        maximum(621,373)
        background 'text_popup_bkgr'
        xalign 0.5
        yalign 0.4
        imagebutton:
            align (1.0, 0.22)
            idle 'input_close'
            hover 'input_close_hover'
            if not randint(0,3):
                action [Hide('text_msg_popup'), deliver_next]
            else:
                action Hide('text_msg_popup')
            
        hbox:
            yalign 0.05
            xalign 0.03
            spacing 15
            add 'new_text_envelope'
            text 'NEW' color '#73f1cf' yalign 1.0 font sans_serif_1b
        
        vbox:
            xalign 0.3
            yalign 0.85
            spacing 20
            hbox:
                spacing 20                
                add Transform(c.prof_pic, size=(110,110))
                
                vbox:
                    spacing 10
                    text "From: " + c.name color '#fff'
                    
                    window:
                        maximum(420,130)
                        background 'text_popup_msg'       
                        text text_popup_preview(last_msg):
                            size 30 
                            xalign 0.5 yalign 0.5 
                            text_align 0.5
            
            if (not (renpy.get_screen('in_call') 
                    or renpy.get_screen('incoming_call') 
                    or renpy.get_screen('outgoing call'))):
                textbutton _('Go to'):
                    text_style 'mode_select'
                    xalign 0.5
                    xsize 220
                    ysize 70
                    text_size 28
                    background 'menu_select_btn' padding(20,20)
                    hover_foreground 'menu_select_btn_hover'
                    if c.real_time_text and c.text_msg.reply_label:
                        action [Hide('text_msg_popup'),
                        Hide('save_load'),
                        Hide('menu'),
                        Hide('chat_footer'),
                        Hide('phone_overlay'),
                        Hide('settings_screen'),
                        SetVariable('CG_who', c),
                        Jump(c.text_msg.reply_label)]
                    else:
                        action [Hide('text_msg_popup'), 
                                SetVariable("current_message", c), 
                                Function(c.text_msg.mark_read),
                                Hide('save_load'),
                                Hide('menu'),
                                Hide('chat_footer'), 
                                Hide('phone_overlay'), 
                                Hide('settings_screen'),
                                SetVariable('CG_who', c),
                                Show('text_message_screen', sender=c)]
            else:
                null height 70
    timer 3.25:
        action If(randint(0,1), [Hide('text_msg_popup', Dissolve(0.25)), 
                                deliver_next], 
                                Hide('text_msg_popup', Dissolve(0.25)))
        
########################################################  
## Includes the 'answer' button at the bottom
########################################################
screen text_message_footer(c):    

    python:
        text_log = c.text_msg.msg_list
        text_read = c.text_msg.read
        text_label = c.text_msg.reply_label
        if len(text_log) > 0:
            last_msg = text_log[-1]
        else:
            last_msg = False

    vbox:
        xalign 0.5
        yalign 1.0
        yoffset -30
        window:
            ymaximum 40
            background 'text_msg_line'
        button:
            xsize 468
            ysize 95
            xalign 0.5
            if text_log and text_label and not last_msg.who.right_msgr:
                background 'text_answer_active'
                hover_background 'text_answer_animation'  
                if not renpy.get_screen("choice"):
                    action Jump(c.text_msg.reply_label)
                    #action Function(c.text_msg.reply)
                    activate_sound "audio/sfx/UI/answer_screen.mp3"
            else:
                background 'text_answer_inactive'
            add 'text_answer_text' xalign 0.5 yalign 0.5
   
## Displays the date separator between two messages that
## have a time difference of one day or more
screen text_date_separator(text_time):

    $ the_time = '20' + text_time.year + '.' + text_time.month_num + '.'
    $ the_time = the_time + text_time.day + ' ' + text_time.weekday
    
    hbox:
        spacing 10
        xalign 0.5
        ysize 80
        xsize 740
        window:
            ymaximum 40
            xmaximum 240
            yalign 0.5
            background 'text_msg_line'
        text the_time size 25 color '#fff' yalign 0.5
        window:
            ymaximum 40
            yalign 0.5
            xmaximum 240
            background 'text_msg_line'
        
########################################################
## This is the screen that actually displays the
## message, though it mostly borrows from the chatroom
## display screen
########################################################

init python:
    def award_text_hp(who):
        who.text_msg.heart_person.increase_heart(who.text_msg.bad_heart)
        renpy.show_screen('heart_icon_screen', 
            character=who.text_msg.heart_person)
        who.text_msg.heart_person = None
        who.text_msg.bad_heart = False
        who.text_msg.heart = False
        store.persistent.HP += 1


screen text_message_screen(sender):

    tag menu
        
    # If this text message is supposed to trigger a heart icon, 
    # display the correctly-coloured heart, award
    # a heart point, and increase the appropriate totals
    if (not sender.real_time_text
            and sender.text_msg.heart
            and not sender.text_msg.msg_list[-1].who.right_msgr):
        on 'show':
            action [Function(award_text_hp, who=sender)]
        on 'replace':
            action [Function(award_text_hp, who=sender)]
        

 

    default prev_msg = None

    use menu_header(sender.name, [SetVariable('CG_who', None),
                                Show('text_message_hub', Dissolve(0.5))], True)

    python:
        yadj.value = yadjValue
        textlog = sender.text_msg.msg_list

        chatLength = len(textlog) - 1
        begin = chatLength - bubbles_to_keep
        if begin >= 0:
            pass
        else:
            begin = 0

    viewport: # viewport id "VP":
        yinitial 1.0
        yadjustment yadj
        draggable True
        mousewheel True
        ysize 1040
        yalign 1.0
        yoffset -144
                        
        has vbox
        spacing 20
        
        for i index id(i) in textlog[begin:]:
            if chatLength > 0 and (prev_msg is not None):
                if i.thetime.day != prev_msg.thetime.day:
                    use text_date_separator(i.thetime) 
            if (len(textlog) > 0
                    and textlog[0] == i):
                use text_date_separator(i.thetime)
            fixed:
                yfit True
                xfit True
                use text_animation(i, False, True)
                use text_animation(i, (sender.real_time_text
                    and i == textlog[-1]))
            $ prev_msg = i
        null height 5
    if not sender.real_time_text:
        use text_message_footer(sender)
    else:
        window:
            xalign 0.5
            ymaximum 40
            yalign 0.905
            background 'text_msg_line'
                


screen text_animation(i, animate=False, anti=False):
    python:       
        transformVar = incoming_message
        if i.who.right_msgr:
            picStyle = 'MC_profpic_text'
            reg_style = 'text_msg_mc_fixed'
            reg_bubble = 'reg_bubble_MC_text'
            hbox_ypos = 5
            img_style = 'mc_img_text_message'
        else:
            picStyle = 'profpic_text'
            reg_style = 'text_msg_npc_fixed'
            reg_bubble = 'reg_bubble_text'
            hbox_ypos = -10
            img_style = 'img_text_message'
                
        ## This determines how long the line of text is. 
        ## If it needs to wrap it, it will pad the bubble 
        ## out to the appropriate length
        ## Otherwise each bubble would be exactly as wide as
        ## it needs to be and no more
        t = Text(i.what)
        z = t.size()
        my_width = int(z[0])
        my_height = int(z[1])
        
        text_time = (i.thetime.twelve_hour 
                        + ':' + i.thetime.minute 
                        + ' ' + i.thetime.am_pm)

        if anti:
            transformVar = invisible
        else:
            transformVar = incoming_message
            
        if not animate and not anti:
            transformVar = null_anim
        
            
    if i.who != 'answer' and i.who != 'pause':        
        # Add the dialogue
        hbox:
            spacing 5 
            if i.who.right_msgr:
                xalign 1.0
                box_reverse True
            xmaximum 750
            style reg_style            
            null width 18
            window:
                style picStyle 
                if not anti and i.who.prof_pic:               
                    add Transform(i.who.prof_pic, size=(110,110))
            
            frame at transformVar:               
                ## Check if it's an image
                if i.img and not "{image=" in i.what:
                    style img_style
                    $ fullsizeCG = cg_helper(i.what)
                    imagebutton:
                        focus_mask True
                        idle smallCG(fullsizeCG)
                        if not choosing:
                            action [SetVariable("fullsizeCG", 
                                        cg_helper(i.what)), 
                                    Call("viewCG", textmsg=True), 
                                    Return()]
        
                
                else:        
                    style reg_bubble
                    yalign 0.0
                    if my_width > gui.longer_than:
                        text i.what:
                            style "bubble_text_long" 
                            min_width gui.long_line_min_width 
                            color '#fff'
                    else:
                        if not i.img:            
                            yoffset 35
                        text i.what style "bubble_text" color '#fff'

            if i != filler and not anti:                 
                text text_time:
                    color '#fff' 
                    yalign 1.0 
                    size 23 
                    if i.img and not "{image=" in i.what:
                        xoffset 10
            
          
                                            
 

        