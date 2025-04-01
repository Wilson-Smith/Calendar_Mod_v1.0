#you need this to work with the calendar
$ import store.mas_calendar as calendar
#list of events that you want added
default persistent.SI_mod_events = []
#Option to add something to the calendar
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="Add_to_callendar",
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
            calendar_event_name = name_month_day[0]
            calendar_event_month = name_month_day[1]
            calendar_event_day = name_month_day[2]
            calendar.addRepeatable(calendar_event_name,_(calendar_event_name),month=int(int(calendar_event_month)),day=int(int(calendar_event_day)),year_param=list())

#adding something to the calendar
label Add_to_callendar:
    #variable to check if the response a player has given is in the correct format(I feel like there is a more elegant solution)
    $ Ok = True
    m 7wub "[player], of course!"
    m 2dua "I know you are a busy guy!"
    m 4wub "Okay! What do you want me to write in the calendar?"
    python:
        calendar_event_name_month_day = renpy.input("Okay! What do you want me to write in the calendar?", length=35)
        if len(calendar_event_name_month_day.split(',')) == 3:
            persistent.SI_mod_events.append(calendar_event_name_month_day)
            name_month_day = persistent.SI_mod_events[-1].split(',')   
            calendar_event_name = name_month_day[0]
            calendar_event_month = name_month_day[1]
            calendar_event_day = name_month_day[2]
            calendar.addRepeatable(calendar_event_name,_(calendar_event_name),month=int(int(calendar_event_month)),day=int(int(calendar_event_day)),year_param=list())
        else:
            Ok = False
            
    if Ok == False:
        m 1etc "Are you sure you typed it correctly?"
        m 3eub "Make sure you have written name,month,day separated by comas!"
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
            #deleting it from the persistent(It would also be good if I could remove it from the calendar right now as well)
            $ del persistent.SI_mod_events[matches[0]]
            m 2dua "When you open the game next time , you will not see it!"
        else:
            m 2lksdlb "That's not supposed to hapen..."
            m 2lksdlb "Probably something is wrong with the code"
    else:
            m 2lksdlb "Strange..."
            m 2eksdlc "I cannot find [calendar_event_name_remove]"
            m 1etc "Are you sure you typed it correctly?"
            

