"""
A command line application to use daily.
It will do the following:
    1. Select a household chore to do that I don't already do daily, weighted by its priority (higher = more frequently picked)
    2. Select 10 flashcards from a topic to review (and append topic to .txt file to keep track of reviewed topics)
    3. Generate a poetry prompt for a short free writing session
    4. Pull a previous day's entry for review before writing a short journal entry
    5. Collect the poetry freewrite and the journal entry into .md file and add it to Obsidian notebook
"""

def select_chore() -> str:
    pass


def select_flashcards() -> dict:
    pass


def generate_prompt() -> str:
    pass


def display_previous_entry() -> str:
    pass


def collect_entry_and_write_to_markdown(poem: str, journal_entry: str) -> None:
    pass


def main():
    pass


if __name__ == "__main__":
    main()