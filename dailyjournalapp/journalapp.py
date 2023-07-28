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
import json
import random


script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = script_dir + '/data/'
notes_dir = script_dir + '/daily_notes/'


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
    filtered_list = [chore for chore in chores_list if chores[chore][0] != chores[chore][1]]
    
    if filtered_list == []:  # if all chores have been completed, restart the cycle
        for chore in chores.keys():
            chores[chore][0] = 0
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
    workout_string = "- [ ] Your workout for today is to do the following exercises:\n"
    workout_string += "    - [ ] " + "\n    - [ ] ".join(workout)
    return workout_string


def select_lens() -> str:
    """
    Accesses procgen_tarot.json, loads it, and randomly selects a card.
    
    Returns string containing the day's reading to use for reflection.
    """
    with open(data_dir + 'procgen_tarot.json') as tarot_file:
        tarot: dict = json.load(tarot_file)
        cards: list = tarot['cards']
    
    card = random.choice(cards)
    lens = f'- Your lens for the day is {card["word"]}.\n- {card["interpretation"]}'
    return lens


def show_project_statuses() -> str:
    with open(data_dir + 'projects_status.json') as project_statuses_file:
        projects: list = json.load(project_statuses_file)['projects']
    
    in_progress = [project for project in projects if project['status'] == 'In Progress']
    statuses = ""
    for project in in_progress:
        project_name = project['project_name']
        subgoals_in_progress = [subgoal for subgoal in project['subgoals'].keys() if project['subgoals'][subgoal] == 'In Progress']
        statuses += "- [ ] " + project_name + "\n    - [ ] " + "\n    - [ ] ".join(subgoals_in_progress) + "\n"
    return statuses


def write_contents_to_markdown(chore: str, 
                               workouts: str, 
                               lens: str,
                               project_statuses: str
                               ) -> None:
    note = (
        "##### Daily Chore:\n" + chore + "\n\n" + 
        "##### Daily Workout Options:\n" + workouts + "\n\n" + 
        "##### Daily Lens:\n" + lens + "\n" +
        "------------------------------------\n"
        "##### Current Project Statuses:\n" + project_statuses
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
    lens: str = select_lens()
    print(lens)
    project_statuses: str = show_project_statuses()
    print(project_statuses)
    
    write_contents_to_markdown(chore=chore,
                              workouts=workout_options,
                              lens=lens,
                              project_statuses=project_statuses)


def update_chores(chore: str) -> None:
    # parse if task is done
    done = (chore[0:5] == '- [x]')
    
    # remove clutter from string
    chore = chore[35:-1]
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'chores.json') as chores_file:
        chores: dict = json.load(chores_file)
    
    if done:
        chores[chore][0] += 1
    
    # export the dictionary to update json
    with open(data_dir + 'chores.json', 'w') as chores_file:
            json.dump(chores, chores_file, indent=2)


def update_workouts(workouts: list) -> None:
    # remove clutter from string
    
    
    # import json as dictionary and then update the dictionary
    with open(data_dir + 'daily_workout.json') as workouts_file:
        workouts: dict = json.load(workouts_file)
    workouts['current_day'] += 1
    workouts['current_day'] %= 7
    
    # export the dictionary to update json
    with open(data_dir + 'daily_workout.json', 'w') as workouts_file:
            json.dump(workouts, workouts_file, indent=2)


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


def update_data_files() -> None:
    current_date = datetime.now()
    date = f'{current_date.year}-{current_date.month}-{current_date.day}'
    
    with open(notes_dir + f"dailynote_{date}.md", "r") as note_file:
        note: str = note_file.read()
    
    lines = note.splitlines()
    
    chore = lines[3]
    update_chores(chore)
    
    workouts = lines[6:8]
    update_workouts(workouts)
    
    project_statuses = lines[14:]
    update_project_statuses(project_statuses)


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
    else:
        pass


if __name__ == "__main__":
    main()
