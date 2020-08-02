init -6 python:

    class TimelineItem(renpy.store.object):
        """
        Parent class which holds information needed to display items on
        the timeline e.g. chatrooms, story mode, phone calls.

        Attributes:
        -----------
        title : string
            Title of this item.
        item_label : string
            Label to jump to to view this item.
        expired_label : string
            Label to jump to when this item has expired.
        trigger_time : string
            Time this item should be available at, if playing in real-time
            mode. Formatted as "00:00" in 24-hour time.
        plot_branch : PlotBranch
            Keeps track of plot branch information if the story should
            branch after this item.
        save_img : string
            A short version of the file path used to display the icon next
            to a save file when this is the active timeline item.
        played : bool
            True if this item has been played.
        available : bool
            True if this item should be available in the timeline.
        expired : bool
            True if this item has expired in the timeline.
        buyback : bool
            True if the player bought this item back after it expired.
        buyahead : bool
            True if the player bought this item ahead of time so it can
            remain unlocked regardless of the current time.
        outgoing_calls_list : string[]
            List of the labels used for phone calls that should follow this
            timeline item. Also used in the History screen.
        incoming_calls_list : string[]
            List of the labels used for incoming phone calls that should
            occur afterr this item. Also used in the History screen.
        story_calls_list : PhoneCall[]
            List of the labels used for mandatory story phone calls that should
            occur after this item. Also used in the History screen.
        """

        def __init__(self, title, item_label, trigger_time, plot_branch="None",
            save_img='auto'):
            
            self.title = title
            self.item_label = item_label

            if plot_branch == "None":
                # There is no plot branch
                self.plot_branch = None
            elif isinstance(plot_branch, PlotBranch):
                self.plot_branch = plot_branch
            elif plot_branch:
                # plot branch should have vn_after_branch=True
                self.plot_branch = PlotBranch(True)
            else:
                self.plot_branch = PlotBranch(False)

            # Ensure the trigger time is set up properly
            # It corrects times like 3:45 to 03:45
            if trigger_time and ':' in trigger_time[:2]:
                self.trigger_time = '0' + trigger_time
            else:
                self.trigger_time = trigger_time
            
            save_img = save_img.lower()
            if save_img in ['jaehee', 'ja']:
                self.save_img = 'jaehee'
            elif save_img in ['jumin', 'ju']:
                self.save_img = 'jumin'
            elif save_img in ['ray', 'r']:
                self.save_img = 'ray'
            elif save_img in ['seven', '707', 's']:
                self.save_img = 'seven'
            elif save_img == 'v':
                self.save_img = 'v'
            elif save_img in ['yoosung', 'y']:
                self.save_img = 'yoosung'
            elif save_img in ['zen', 'z']:
                self.save_img = 'zen'
            elif save_img[:5] == "save_":
                self.save_img = save_img[5:]
            else:
                # e.g. auto / another / april / casual / deep / xmas
                self.save_img = save_img

            self.expired_label = item_label + "_expired"
            self.played = False
            self.available = False
            self.expired = False
            self.buyback = False
            self.buyahead = False

            self.outgoing_calls_list = [ (self.item_label + '_outgoing_' 
                + x.file_id) for x in store.all_characters 
                if renpy.has_label(self.item_label + '_outgoing_' 
                    + x.file_id)]
            self.incoming_calls_list = [ (self.item_label + '_incoming_' 
                + x.file_id) for x in store.all_characters 
                if renpy.has_label(self.item_label + '_incoming_' 
                    + x.file_id)]

            self.story_calls_list = [
                    PhoneCall(x, 
                    self.item_label + '_story_call_' + x.file_id,
                    avail_timeout='test', story_call=True)
                for x in store.all_characters 
                    if renpy.has_label(self.item_label + '_story_call_'
                        + x.file_id)]
            

        def __eq__(self, other):
            """Check for equality between two TimelineItem objects."""

            if not isinstance(other, TimelineItem):
                return False
            return (self.title == other.title
                    and self.item_label == other.item_label
                    and self.trigger_time == other.trigger_time)

        def __ne__(self, other):
            """Check for inequality between two TimelineItem objects."""

            if not isinstance(other, TimelineItem):
                return True
            return (self.title != other.title
                    or self.item_label != other.item_label
                    or self.triggger_time != other.trigger_time)

        
    class ChatRoom(TimelineItem):
        """
        Class that stores information needed to display chatrooms in-game.

        Attributes:
        -----------
        participants : ChatCharacter[]
            List of ChatCharacters who were present over the course of this
            chatroom. Initially set to the characters who begin in the chat.
        original_participants : ChatCharacter[]
            List of ChatCharacters who begin in the chatroom.
        story_mode : StoryMode
            Contains the information for a Story Mode section following
            this chatroom.
        participated : bool
            True if the player participated in this chatroom.
        replay_log : ReplayEntry
            List of ReplayEntry objects that keeps track of how this chatroom
            played out to display to the player during a replay.        
        """

        def __init__(self, title, chatroom_label, trigger_time,
                participants=None, story_mode=None, plot_branch="None",
                save_img='auto'):
            """
            Create a ChatRoom object to store information about a particular
            chatroom on a route.

            Parameters:
            -----------
            title : string
                Title of the chatroom.
            chatroom_label : string
                Label to jump to to view this chatroom.
            trigger_time : string
                Time this chatroom should be available at, if playing in
                real-time. Formated as "00:00" in 24-hour time.
            participants : ChatCharacter[]
                List of ChatCharacters who were present over the course of
                this chatroom. Initially set to the characters who begin in
                the chat.
            story_mode : StoryMode
                Contains the information for a StoryMode section that follows
                this chatroom.
            plot_branch : bool
                True if this chatroom should have a plot branch following it
                and the StoryMode associated with the chatroom should appear
                after the plot branch has been proceeded through; False if 
                there is a plot branch but no corresponding StoryMode.
            save_img : string
                A short version of the file path used to display the icon next
                to a save file when this is the active timeline item.
            """

            super(ChatRoom, self).__init__(title, chatroom_label, trigger_time,
                plot_branch, save_img)
            
            print("ChatRoom label:", self.item_label)
            self.participants = participants or []
            if len(self.participants) == 0:
                self.original_participants = []
            else:
                self.original_participants = list(participants)

            self.story_mode = None
            if story_mode:
                self.story_mode = story_mode
            else:
                # Check for labels to auto-define StoryMode objects
                # First check for the default VN with no associated character
                if renpy.has_label(self.item_label + '_vn'):
                    self.story_mode = create_dependent_VN(
                        self.item_label + '_vn')
                    print("Looked for label", self.item_label + '_vn')
                # Check for a party label
                elif renpy.has_label(self.item_label + '_party'):
                    self.story_mode = create_dependent_VN(
                        self.item_label + '_party',
                        party=True)
                    print("Looked for label", self.item_label + '_party')
                # Check for VNs associated with a character
                else:                    
                    for c in store.all_characters:
                        # VNs are called things like my_label_vn_r
                        vnlabel = self.item_label + '_vn_' + c.file_id
                        if renpy.has_label(vnlabel):
                            self.story_mode = create_dependent_VN(vnlabel, c)
                            print("Looked for label", vnlabel)
                            # Should only be one StoryMode object per chat
                            break
                if self.story_mode:
                    print("Tried to create StoryMode object:", self.story_mode)

            if self.plot_branch and self.plot_branch.vn_after_branch:
                self.plot_branch.stored_vn = self.story_mode
                self.story_mode = None

            self.participated = False
            self.replay_log = []

        def add_participant(self, chara):
            """Add a participant to the chatroom."""

            if not (chara in self.participants):
                self.participants.append(chara)
            return
        
        def reset_participants(self):
            """
            Reset participants to the original set of participants before
            the user played this chatroom. Used when a player backs out
            of a chatroom.
            """

            self.participants = list(self.original_participants)

    class StoryMode(TimelineItem):
        """
        Class that stores information needed to display StoryMode objects
        in-game.

        Attributes:
        -----------
        who : string
            The character's file_id whose picture is on the StoryMode icon
            in the timeline.
        party : bool
            True if this StoryMode leads to the party.
        """

        def __init__(self, title, vn_label, trigger_time, who=None,
                plot_branch="None", party=False, save_img='auto'):
            """
            Create a StoryMode object to keep track of information for a 
            Story Mode section.

            Parameters:
            -----------
            title : string
                The title of this story mode section.
            vn_label : string
                The label to jump to to play this story mode.
            trigger_time : string
                Formatted as "00:00" in 24-hour time. The time this story
                mode should appear at, if it is not attached to a chatroom.
            who : ChatCharacter
                The character whose picture is on the StoryMode icon in
                the timeline.
            plot_branch : bool
                True if this chatroom should have a plot branch following it
                and the StoryMode associated with the chatroom should appear
                after the plot branch has been proceeded through; False if 
                there is a plot branch but no corresponding StoryMode.
            party : bool
                True if this story mode leads to the party.
            save_img : string
                A short version of the file path used to display the icon next
                to a save file when this is the active timeline item.
            """

            super(StoryMode, self).__init__(title, vn_label, trigger_time, plot_branch,
                save_img)

            if who is not None:
                self.who = who.file_id
            else:
                self.who = None
            self.party = party

        


    def create_dependent_VN(vn_label, who=None, party=False):
        """
        Return a VN which is tied to a chatroom and thus doesn't need
        additional information.
        """
        print("Making a StoryMode", vn_label)
        return StoryMode(title="", vn_label=vn_label, trigger_time=False,
                who=who, party=party)

    def chathistory_to_chatroom(item, copy_everything=False):
        """Convert item to a ChatRoom object and return it."""

        print("LOOKING AT:", item.title)

        if (item.plot_branch and item.plot_branch.stored_vn):
            pbranch = True
        elif isinstance(item.plot_branch, PlotBranch):
            pbranch = False
        else:
            pbranch = "None"

        if pbranch != "None":
            print("pbranch is", pbranch)

        new_obj = ChatRoom(title=item.title, chatroom_label=item.chatroom_label,
            trigger_time=item.trigger_time, participants=item.participants,
            plot_branch=pbranch, save_img=item.save_img)

        
        if copy_everything:
            # Need to check all other fields as well
            # It's okay to copy list addresses since the program won't be
            # using the originals any more
            new_obj.original_participants = item.original_participants
            new_obj.played = item.played
            new_obj.participated = item.participated
            new_obj.available = item.available
            new_obj.expired = item.expired
            new_obj.buyback = item.buyback
            new_obj.buyahead = item.buyahead
            new_obj.replay_log = item.replay_log
           

        # Test to see if the two items are the same
        if item.title != new_obj.title:
            print("title:", item.title, new_obj.title)
        if item.chatroom_label != new_obj.item_label:
            print("label:", item.chatroom_label, new_obj.item_label)
        if item.expired_chat != new_obj.expired_label:
            print("expired:", item.expired_chat, new_obj.expired_label)
        if item.trigger_time != new_obj.trigger_time:
            print("time:", item.trigger_time, new_obj.trigger_time)
        if item.participants != new_obj.participants:
            print("participants:", item.participants, new_obj.participants)
        if (item.plot_branch != new_obj.plot_branch
                and not (item.plot_branch == False 
                    and new_obj.plot_branch is None)):
            print("plot_branch:", item.plot_branch, new_obj.plot_branch)
        if (item.plot_branch and item.plot_branch.stored_vn):
            if (item.plot_branch.stored_vn.vn_label 
                    != new_obj.plot_branch.stored_vn.item_label):
                print("plot_branch stored VN:", item.plot_branch.stored_vn.vn_label,
                    new_obj.plot_branch.stored_vn.item_label)
        if (item.vn_obj and new_obj.story_mode):
            if item.vn_obj.vn_label != new_obj.story_mode.item_label:
                print("vn/story mode:", item.vn_obj.vn_label, 
                    new_obj.story_mode.item_label)
        if (item.vn_obj and not new_obj.story_mode):
            print("\ \ \ So we don't have an equivalent story mode for some reason")
            print("vn/story mode:", item.vn_obj, new_obj.story_mode)
        if item.save_img != new_obj.save_img:
            print("save_img:", item.save_img, new_obj.save_img)
        if item.played != new_obj.played:
            print("played:", item.played, new_obj.played)
        if item.participated != new_obj.participated:
            print("participated:", item.participated, new_obj.participated)
        if item.available != new_obj.available:
            print("available:", item.available, new_obj.available)
        if item.expired != new_obj.expired:
            print("expired:", item.expired, new_obj.expired)
        if item.buyback != new_obj.buyback:
            print("buyback:", item.buyback, new_obj.buyback)
        if item.buyahead != new_obj.buyahead:
            print("buyahead:", item.buyahead, new_obj.buyahead)
        if item.outgoing_calls_list != new_obj.outgoing_calls_list:
            print("outgoing_calls_list:", item.outgoing_calls_list, new_obj.outgoing_calls_list)
        if item.incoming_calls_list != new_obj.incoming_calls_list:
            print("incoming_calls_list:", item.incoming_calls_list, new_obj.incoming_calls_list)
        if item.story_calls_list != new_obj.story_calls_list:
            print("story_calls_list:", item.story_calls_list, new_obj.story_calls_list)

        return new_obj
        