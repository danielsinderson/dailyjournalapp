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
    with open(script_dir + '/chores.json') as chores_file:
        chores = json.load(chores_file)
    
    chores_list = [chore * chores[chore] for chore in chores.keys()]
    return random.choice(chores_list)


def select_flashcards() -> dict:
    return {}


def generate_prompt() -> str:
    return ''


def select_previous_entry() -> str:
    return ''


def display_contents(chore: str, 
                     flashcards: dict, 
                     prompt: str,
                     previous_entry: str
                     ) -> tuple:
    return ('', '')


def collect_entry_and_write_to_markdown(poem: str, journal_entry: str) -> None:
    pass


def main():
    chore: str = select_chore()
    print(chore)
    flashcards: dict = select_flashcards()
    prompt: str = generate_prompt()
    previous_entry: str = select_previous_entry()
    
    result: tuple = display_contents(chore, 
                                    flashcards,
                                    prompt,
                                    previous_entry)
    
    collect_entry_and_write_to_markdown(result[0], result[1])


if __name__ == "__main__":
    main()