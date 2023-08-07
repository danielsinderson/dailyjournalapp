"""
A command line application to use daily.
It will do the following:
    1. Select a household chore to do that I don't already do daily, weighted by its priority (higher = more frequently picked)
    2. Select 10 flashcards from a topic to review (and append topic to .txt file to keep track of reviewed topics)
    3. Generate a poetry prompt for a short free writing session
    4. Pull a previous day's entry for review before writing a short journal entry
    5. Collect the poetry freewrite and the journal entry into .md file and add it to Obsidian notebook
    6. Print out current state of projects (track progress in json)
"""

import sys
import os
from datetime import datetime
from datetime import timedelta
import json
import random


script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = script_dir + '/data/'
notes_dir = script_dir + "/daily_notes/"
daily_note_dir = script_dir + "/daily_notes/"
dad_note_dir = script_dir + "/dad_notes/"



def select_chore() -> str:
    """
    Accesses chores.json, loads it, and randomly selects a chore based on weighting.
    
    Returns string containing the chore to do that day
    """
    with open(data_dir + 'chores.json') as chores_file:
        chores: dict = json.load(chores_file)
    
    # create a list of chores 
    chores_list = [chore for chore in chores.keys()]
    #filter out the chores that have already been completed this cycle
    filtered_list = [chore for chore in chores_list if 
                     chores[chore]['count'] != chores[chore]['frequency'] and 
                     chores[chore]['countdown'] == 0]
    
    
    if filtered_list == []:  # if all chores have been completed, restart the cycle
        for chore in chores.keys():
            chores[chore]['count'] = 0
        chore = random.choice(chores_list)
    else:  # else pick one of the remaining chores at random
        chore = random.choice(filtered_list)
    
    return f'- [ ] Your chore for the day is to {chore}.'


def select_workouts() -> str:
    """
    Accesses daily_workout.json, loads it, and randomly selects a light and regular workout.
    
    Returns string containing the workout options to do that day
    """
    with open(data_dir + 'daily_workout.json') as workouts_file:
        workouts: dict = json.load(workouts_file)
    
    day = workouts['current_day']
    workout = workouts['schedule'][day]
    workout_string = f"- [ ] Your workout for today is a {workout} workout."
    return workout_string


def show_appointments() -> str :
    # load appointments.json into dictionary
    with open(data_dir + 'appointments.json') as appointments_file:
        appointments: dict = json.load(appointments_file)
    
    # get current date
    current_date = datetime.now()
    date = f'{current_date.month}-{current_date.day}'
    
    # get appointments that are happening on the current date
    appointments_today = []
    for appointment in appointments.keys():
        appointment_date = appointments[appointment]["date"].split(' ')[0]
        appointment_time = appointments[appointment]["date"].split(' ')[1]
        if appointment_date == date:
            name = appointment
            appointments_today.append(f"{name} at {appointment_time}")
    
    reminders = "You have the following appointments today\n- " + "\n- ".join(appointments_today) + "\n"
    return reminders
    

def show_project_statuses() -> str:
    with open(data_dir + 'projects_status.json') as project_statuses_file:
        projects: list = json.load(project_statuses_file)['projects']
    
    in_progress = [project for project in projects if project['status'] == 'In Progress']
    statuses = ""
    for project in in_progress:
        project_name = project['project_name']
        subgoals_in_progress = [subgoal for subgoal in project['subgoals'].keys() if project['subgoals'][subgoal] == 'In Progress']
        statuses += "- [ ] " + project_name + "\n    - [ ] " + "\n    - [ ] ".join(subgoals_in_progress[:3]) + "\n"
    return statuses


def show_special_events() -> str:
    with open(data_dir + 'special_events.json') as events_file:
        events: list = json.load(events_file)['events']
    
    current_date = datetime.now()
    date = f'{current_date.month}-{current_date.day}-{current_date.year}'
    
    reminders_today = []
    for event in events:
        d = event['date'].split('-')
        month_of_event = int(d[0])
        day_of_event = int(d[1])
        year_of_event = int(d[2])
        event_date = datetime(year=year_of_event, month=month_of_event, day=day_of_event)
        delta = event_date - current_date
        
        if delta.days == -1:
            reminders_today = [f"{event['name']} is today!"] + reminders_today
        elif delta.days == 0:
            reminders_today = [f"{event['name']} is tomorrow!"] + reminders_today
        elif delta.days <= event['reminder']:
            reminders_today = reminders_today + [f"{event['name']} will be on {event['date']}, just {delta.days + 1} days away."]
    
    reminders = "The following special events with happen soon!\n- " + "\n- ".join(reminders_today) + "\n"
    return reminders
    

def write_contents_to_markdown(chore: str, 
                               workouts: str, 
                               appointments: str,
                               project_statuses: str,
                               special_events: str
                               ) -> None:
    note = (
        "##### Daily Chore:\n" + chore + "\n" + 
        "------------------------------------\n" + 
        "##### Daily Workout:\n" + workouts + "\n" + 
        "------------------------------------\n" + 
        "##### Appointments:\n" + appointments +
        "------------------------------------\n" + 
        "##### Special Events:\n" + special_events +
        "------------------------------------\n" + 
        "##### Current Project Statuses:\n" + project_statuses + 
        "------------------------------------\n" + 
        "##### Notes:\n## \n" +
        "------------------------------------\n" + 
        "##### Dad Notes:\n## \n"
    )
    current_date = datetime.now()
    date = f'{current_date.year}-{current_date.month}-{current_date.day}'
    with open(notes_dir + f"dailynote_{date}.md", "w") as note_file:
        note_file.write(f"Daily note for {date}:\n\n" + note)


def create_new_entry() -> None:
    chore: str = select_chore()
    print(chore)
    
    workout_options: str = select_workouts()
    print(workout_options)
    
    appointments: str = show_appointments()
    print(appointments)
    
    events: str = show_special_events()
    print(events)
    
    project_statuses: str = show_project_statuses()
    print(project_statuses)
    
    write_contents_to_markdown(chore=chore,
                              workouts=workout_options,
                              appointments=appointments,
                              project_statuses=project_statuses,
                              special_events=events)


def update_chores(chore: str) -> None:
    # parse if task is done
    done = (chore[0:5] == '- [x]')
    
    # remove clutter from string
    chore = chore[35:-1]
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'chores.json') as chores_file:
        chores: dict = json.load(chores_file)
    
    if done:
        chores[chore]['count'] += 1
        chores[chore]['countdown'] = chores[chore]['delay']
    
    for c in chores:
        if c != chore and chores[c]['countdown'] > 0:
            chores[c]['countdown'] -= 1
    
    # export the dictionary to update json
    with open(data_dir + 'chores.json', 'w') as chores_file:
            json.dump(chores, chores_file, indent=2)


def update_workouts(workout: str) -> None:
    # parse if done
    done = (workout[0:5] == '- [x]')
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'daily_workout.json') as workouts_file:
        workouts: dict = json.load(workouts_file)
    
    if done:
        workouts['current_day'] += 1
        workouts['current_day'] %= 7
    
    # export the dictionary to update json
    with open(data_dir + 'daily_workout.json', 'w') as workouts_file:
            json.dump(workouts, workouts_file, indent=2)


def update_appointments(appointments: list) -> None:
    # parse appointments
    done_appointments = [appointment[2:-9] for appointment in appointments]
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'appointments.json') as appointments_file:
        appointments: dict = json.load(appointments_file)
    
    appointments_to_delete = []
    for appointment in appointments.keys():
        if appointment not in done_appointments:
            continue
        
        if appointments[appointment]["recurring"]:
            time = appointments[appointment]["date"].split(' ')[1]
            new_date = datetime.now() + timedelta(days=7)
            appointments[appointment]["date"] = f"{new_date.month}-{new_date.day} {time}"
        else: 
            appointments_to_delete += [appointment]
    
    for appointment in appointments_to_delete:
        del appointments[appointment]
        
    # export the dictionary to update json
    with open(data_dir + 'appointments.json', 'w') as appointments_file:
            json.dump(appointments, appointments_file, indent=2)

def update_project_statuses(statuses: list) -> None:
    # parse the statuses of the project goals / subgoals from the day to see what got done
    parsed_statuses = {}
    
    for status in statuses:
        subgoal = (status[0:4] == '    ')
        completed = (status[0:9] == '    - [x]') if subgoal else (status[0:5] == '- [x]')
        task = status[10:] if subgoal else status[6:]
        parsed_statuses[task] = { 'is_subgoal': subgoal, 'is_completed': completed }    
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'projects_status.json') as status_file:
        statuses: dict = json.load(status_file)
    
    for project_task, project_status in parsed_statuses.items():
        if not project_status['is_completed']:
            continue
        
        for project in statuses['projects']:
            if project_status['is_subgoal']:
                for subgoal in project['subgoals'].keys():
                    if subgoal == project_task:
                        project['subgoals'][subgoal] = 'Complete'
            else: 
                if project['project_name'] == project_task:
                    project['status'] = 'Complete'
            
    # export the dictionary to update json
    with open(data_dir + 'projects_status.json', 'w') as status_file:
            json.dump(statuses, status_file, indent=2)


def update_special_events(special_events: list):
    # find events that happened that day
    passed_events = [event[2:-10] for event in special_events if event[-6:] == "today!"]
            
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'special_events.json') as events_file:
        events: dict = json.load(events_file)
    
    for event in events['events']:
        for passed_event in passed_events:
            if event['name'] == passed_event:
                date = event['date'].split('-')
                date[2] = str(int(date[2]) + 1)
                event['date'] = '-'.join(date)
    
    # export the dictionary to update json
    with open(data_dir + 'special_events.json', 'w') as events_file:
            json.dump(events, events_file, indent=2)
                

def update_notes(notes: list, date: str) -> None:
    if notes == ['## ']:
        return
    
    title = notes[0][3:]
    note = "\n".join(notes) + f"\n\n{date}"
    with open(daily_note_dir + title + ".md", 'w') as note_file:
        note_file.write(note)


def update_dad_notes(dad_notes: list, date: str) -> None:
    if dad_notes == ['## ']:
        return
    
    title = date + dad_notes[0][3:]
    note = "\n".join(dad_notes) + f"\n\n{date}"
    with open(dad_note_dir + title + ".md", 'w') as note_file:
        note_file.write(note)


def update_data_files() -> None:
    current_date = datetime.now()
    date = f'{current_date.year}-{current_date.month}-{current_date.day}'
    
    with open(notes_dir + f"dailynote_{date}.md", "r") as note_file:
        note: str = note_file.read()
    
    sections = note.split("------------------------------------\n")
    
    chore = sections[0].splitlines()[3]
    update_chores(chore)
    
    workout = sections[1].splitlines()[1]
    update_workouts(workout)
    
    appointments = sections[2].splitlines()[2:]
    print(appointments)
    update_appointments(appointments)
    
    special_events = sections[3].splitlines()[1:]
    update_special_events(special_events)
    
    project_statuses = sections[4].splitlines()[1:]
    update_project_statuses(project_statuses)
    
    notes = sections[5].splitlines()[1:]
    update_notes(notes, date)
    
    dad_notes = sections[6].splitlines()[1:]
    update_dad_notes(dad_notes, date)
    

def delete_entry() -> None:
    current_date = datetime.now()
    date = f'{current_date.year}-{current_date.month}-{current_date.day}'
    os.remove(notes_dir + f"dailynote_{date}.md")


def main():
    if len(sys.argv) < 2:
        print("Sorry, you didn't specify a parameter")
        print(f"The correct format is journalapp.py CREATE|UPDATE")
        sys.exit()
    
    option = sys.argv[1]

    if option == "create":
        create_new_entry()
    elif option == "update":
        update_data_files()
        delete_entry()
    else:
        pass


if __name__ == "__main__":
    main()