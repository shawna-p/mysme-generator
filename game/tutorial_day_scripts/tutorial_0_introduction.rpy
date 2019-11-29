﻿label start():
    
    # This variable is set here simply so you can use the Save & Exit
    # function after your intro chatroom. You don't need to change these
    # values. You can, however, make a label called 'after_starter_chat'
    # to include text messages, or a phone call label called something
    # like 'starter_chat_incoming_ja'. You can't have VNs after this chatroom,
    # but it's possible to have VN sections mid-chatroom using 'call' or
    # to write a VN section before starting the chatroom
    $ current_chatroom = Chat_History('Starter Chat', 'starter_chat', '00:00')
    # This sets a specific variable that lets you have phone calls/
    # VNs for this specific starter chat/opening
    $ starter_story = True
    
    # If you'd like to begin with a phone call, this is
    # how you'll do it. Just replace 'u' with whatever
    # character you want to call you
    call new_incoming_call(Phone_Call(u, 'n/a')) 
    
    # Begin and end the phone call like you would anywhere else
    call phone_begin 
    
    u_phone """
    
    Oh! You picked up; I'm so relieved.
    
    I thought maybe you wouldn't since my number wouldn't be listed in your phone.
    
    I'm calling because I was hoping you could help me test a new app I made. What do you think?
    
    """
    menu:
        extend ''
        "Testing? What would I need to do?":
            m_phone "Testing? What would I need to do?"
        "Sounds like a lot of work.":
            m_phone "Sounds like a lot of work."
            u_phone "Oh, it's not bad, I promise!"
        "I've actually already seen this; can you take me to the home screen?" if persistent.HP:
            m_phone "I've actually already seen this; can you take me to the home screen?"
            u_phone "Oh, sure! See you later~"
            $ persistent.first_boot = False
            $ persistent.on_route = True
            call press_save_and_exit(False)
            
    u_phone """
    
    All you have to do is use the app, and then you let me know if you run into problems or bugs.
    
    It'll help me make a much better program, in the end.
    
    You only need to do as much as you have time for. And in return you get to test out my program earlier than anyone else!
    
    So what do you say?
    
    """
    
    menu:
        extend ''
        "I suppose I'll give it a shot.":
            m_phone "I suppose I'll give it a shot."
            
    u_phone """
    
    You will? Wonderful!
    
    Alright, so when this call ends I'll send you a chatroom message with a bit more information.
    
    Good luck!
    
    """
    
    # Note that this is 'call' instead of 'jump'; this
    # allows us to continue on with a chatroom instead of
    # ending the introduction here
    call phone_end 
    # This ensure the transition from phone to chatroom is smoother
    scene bg black
    
    # Instead of ending the label here, we'll continue with
    # a chatroom. If you don't want the phonecall beforehand,
    # just delete that section
    # Feel free to modify the chatroom beyond this point
    call hack 
    call chat_begin('hack') 
        
    call play_music(mystic_chat)
    
    call enter(u) 
    u "You're here!" 
    u "Thank you for helping me ^^" 
    u "As you can see, this is a sort of \"introductory\" chatroom. It works a lot like the other chatrooms," 
    u "but with a couple of changes you can see in {b}tutorial_0_introduction.rpy{/b}" 
    u "I recommend you get familiar with how regular chatrooms and phonecalls work before you look at this chat, though!" 
    
    call answer 
    menu:
        "What should I look at first?":
            m "What should I look at first?"   (pauseVal=0)
            u "Well, the first thing I recommend is to just play through the Tutorial Day." 
            u "It showcases some of the features so you know what sorts of things you can do with the program." 
    
    
    u "I won't keep you much longer. Enjoy the program!" 
    call exit(u) 
    
    jump chat_end


