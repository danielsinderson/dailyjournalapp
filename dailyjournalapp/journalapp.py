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

import os
import datetime
import json
import random


script_dir = os.path.dirname(os.path.abspath(__file__))


def select_chore() -> str:
    """
    Accesses chores.json, loads it, and randomly selects a chore based on weighting.
    
    Returns string containing the chore to do that day
    """
    with open(script_dir + '/data/chores.json') as chores_file:
        chores: dict = json.load(chores_file)
    
    chores_list = [chore for chore in chores.keys() for i in range(chores[chore])]
    return f'Your chore for the day is to {random.choice(chores_list)}.'


def select_workouts() -> str:
    """
    Accesses daily_workout.json, loads it, and randomly selects a light and regular workout.
    
    Returns string containing the workout options to do that day
    """
    with open(script_dir + '/data/daily_workout.json') as workouts_file:
        workouts: dict = json.load(workouts_file)
    
    light_workout = random.choice(workouts["light workouts"])
    workout = random.choice(workouts["workouts"])
    workout_options = f'Your light workout option is to do a {light_workout} ' \
        f'and your regular workout option is to do a {workout}. ' \
        f'If you feel like going for a heavier workout, just increase the intensity of either one and/or do both.'
    return workout_options


def select_lens() -> str:
    """
    Accesses procgen_tarot.json, loads it, and randomly selects a card.
    
    Returns string containing the day's reading to use for reflection.
    """
    with open(script_dir + '/data/procgen_tarot.json') as tarot_file:
        tarot: dict = json.load(tarot_file)
        cards: list = tarot['cards']
    
    card = random.choice(cards)
    lens = f'Your lens for the day is {card["word"]}. {card["interpretation"]}'
    return lens


def select_previous_entry() -> str:
    return ''


def show_project_statuses() -> str:
    with open(script_dir + '/data/projects_status.json') as project_statuses_file:
        projects: list = json.load(project_statuses_file)['projects']
    
    in_progress = [project for project in projects if project['status'] == 'In Progress']
    statuses = ""
    for project in in_progress:
        project_name = project['project_name']
        subgoals_in_progress = [subgoal['subgoal_name'] for subgoal in project['subgoals'] if subgoal['status'] == 'In Progress']
        statuses += "\n\n" + project_name + "\n - " + "\n - ".join(subgoals_in_progress)
    return statuses


def write_contents_to_markdown(chore: str, 
                               workouts: str, 
                               lens: str,
                               previous_entry: str,
                               project_statuses: str
                               ) -> None:
    pass


def main():
    chore: str = select_chore()
    print(chore)
    workout_options: str = select_workouts()
    print(workout_options)
    lens: str = select_lens()
    print(lens)
    project_statuses: str = show_project_statuses()
    print(project_statuses)
    previous_entry: str = select_previous_entry()
    
    write_contents_to_markdown(chore=chore,
                               workouts=workout_options,
                               lens=lens,
                               previous_entry=previous_entry,
                               project_statuses=project_statuses)


if __name__ == "__main__":
    main()