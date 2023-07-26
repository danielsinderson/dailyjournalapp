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


def select_chore() -> str:
    """
    Accesses chores.json, loads it, and randomly selects a chore based on weighting.
    
    Returns string containing the chore to do that day
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(script_dir + '/data/chores.json') as chores_file:
        chores: dict = json.load(chores_file)
    
    chores_list = [chore for chore in chores.keys() for i in range(chores[chore])]
    return random.choice(chores_list)


def select_workouts() -> list:
    """
    Accesses daily_workout.json, loads it, and randomly selects a light and regular workout.
    
    Returns string containing the workout options to do that day
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(script_dir + '/data/daily_workout.json') as workouts_file:
        workouts: dict = json.load(workouts_file)
    
    light_workout = '\n'.join(random.choice(workouts["light workouts"]))
    workout = '\n'.join(random.choice(workouts["workouts"]))
    
    return [light_workout, workout]


def select_lens() -> str:
    """
    Accesses procgen_tarot.json, loads it, and randomly selects a card.
    
    Returns string containing the day's reading to use for reflection.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(script_dir + '/data/procgen_tarot.json') as tarot_file:
        tarot: dict = json.load(tarot_file)
        cards: list = tarot['cards']
    
    card = random.choice(cards)
    return card


def select_previous_entry() -> str:
    return ''


def write_contents_to_markdown(chore: str, 
                               workouts: str, 
                               lens: str,
                               previous_entry: str
                               ) -> None:
    pass


def main():
    chore: str = select_chore()
    print(chore)
    workout_options: list = select_workouts()
    print(workout_options)
    lens: str = select_lens()
    print(lens)
    previous_entry: str = select_previous_entry()
    
    write_contents_to_markdown(chore=chore,
                               workouts=workout_options,
                               lens=lens,
                               previous_entry=previous_entry)


if __name__ == "__main__":
    main()