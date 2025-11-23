#you need this to work with the calendar
$ import store.mas_calendar as calendar

#list of events that you want added
init -1 python:
    if not hasattr(persistent, "SI_mod_events"):
        persistent.SI_mod_events = []

#Option to add something to the calendar
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="Add_to_calendar",
            prompt="Can you add something to your calendar?",
            category=["Self-improvement"],
            pool=True,
            unlocked=True
        )
    )

#Adding events to the calendar everytime you open a game
init 5 python:
    for item in persistent.SI_mod_events:
        #splitting the input to the event name , month and a day
        name_month_day = item.split(',')
        #if it contains a name ,month and a day then add them to the calendar
        if len(name_month_day) == 3:
            calendar_event_name = name_month_day[0].strip()
            calendar_event_month = name_month_day[1]
            calendar_event_day = name_month_day[2]
            if calendar_event_name:
                try:
                    calendar_event_month = int(calendar_event_month)
                    calendar_event_day = int(calendar_event_day)
                except Exception:
                    continue
                #if calendar_event_month.type()=='int':
                if calendar_event_month >= 1 and calendar_event_month <= 12:  
                    max_day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][calendar_event_month - 1]
                    #if calendar_event_day.type()=='int'
                    if calendar_event_day >= 1 and calendar_event_day <= max_day:
                        calendar.addRepeatable(
                            calendar_event_name,
                            _(calendar_event_name),
                            month=calendar_event_month,
                            day=calendar_event_day,
                            year_param=list()
                            )

#adding something to the calendar
label Add_to_calendar:
    m 7wub "[player], of course!"
    m 2dua "I know you are a busy guy!"
    m 4dua "Okay! Let's get the details down."
    
    # --- INPUT 1: NAME ---
    $ event_name = renpy.input("What is the name of the event?", length=40).strip()
    
    if event_name == "":
        m 1eksdlc "Oh, you didn't say anything..."
        m 1eka "We can try again later."
        return

    # --- INPUT 2: MONTH ---
    m 2eub "Got it, [event_name]! And which month is that in?"
    # allow="0123456789" ensures only numbers can be typed
    $ event_month_str = renpy.input("Month (1-12)", allow="0123456789", length=2).strip()
    
    if event_month_str == "":
        m 1eksdlc "I need a month to write it down..."
        return

    # --- INPUT 3: DAY ---
    m 2eub "Okay, month [event_month_str]. And the day?"
    $ event_day_str = renpy.input("Day (1-31)", allow="0123456789", length=2).strip()

    if event_day_str == "":
        m 1eksdlc "I need the day too!"
        return

    # --- VALIDATION AND SAVING ---
    python:
        isValid = False
        error_message = ""
        
        try:
            event_month = int(event_month_str)
            event_day = int(event_day_str)
            
            if event_month < 1 or event_month > 12:
                error_message = "The month has to be between 1 and 12."
            else:
                max_day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][event_month - 1]
                if event_day < 1 or event_day > max_day:
                    error_message = "Month {} only has {} days.".format(event_month, max_day)
                else:
                    isValid = True
        except ValueError:
             error_message = "That doesn't look like a valid number..."

    if isValid:
        # We construct the comma-separated string just like before so the init block can read it
        $ persistent_entry = "{},{},{}".format(event_name, event_month, event_day)
        
        # Add to persistent storage
        $ persistent.SI_mod_events.append(persistent_entry)
        
        # Add to the active calendar immediately
        $ calendar.addRepeatable(event_name, _(event_name), month=event_month, day=event_day, year_param=list())
        
        m 2dua "Done! I've added [event_name] to the calendar on [event_month]/[event_day]."
        m 4eub "Thanks for telling me!"
    else:
        m 2lksdlb "Wait a second..."
        m "[error_message]"
        m 1eka "Let's try that again when you're ready."

    return

#option to remove something from the calendar
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="Remove_from_calendar",
            prompt="Can you remove something from your calendar?",
            category=["Self-improvement"],
            pool=True,
            unlocked=True
        )
    )
#Removing from the calendar
label Remove_from_calendar:
    m 7esb "Okay!"
    $ calendar_event_name_remove = renpy.input("Okay! What do you want me to remove from the calendar?", length=40)
    #Getting the index of the elements with the same name 
    $ matches = [i for i, item in enumerate(persistent.SI_mod_events) if item.split(",")[0] == calendar_event_name_remove]
    if matches:
        m 2dua "Found it!"
        # Check if the index is valid before removing
        if 0 <= matches[0] < len(persistent.SI_mod_events):
            #deleting it from the persistent
            $ del persistent.SI_mod_events[matches[0]]
            m 2dua "When you open the game next time, you will not see it!"
            m 2eka "I can't remove it from the calendar view instantly, but it is gone from my list."
        else:
            m 2lksdlb "That's not supposed to happen..."
            m 2lksdlb "Probably something is wrong with the code"
    else:
            m 2lksdlb "Strange..."
            m 2eksdlc "I cannot find [calendar_event_name_remove]"
            m 1etc "Are you sure you typed it correctly?"
    return