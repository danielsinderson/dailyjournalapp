"""
Generate prompts for poems.
"""

import random


def generate_constraints(rhyming=False) -> str:
    operators = ['~', '=', '<=']
    meters = ['iambic', 'trochaic']
    rhyme_types = ['true', 'slant', 'assonant', 'consonant']
    rhyme_scheme = ['alternating', 'coupled', 'irregular']
    
    lines = f"The poem will have {random.choice(operators)}{random.randint(2, 16)} lines."
    stresses = f'The poem will have {random.choice(operators)}{random.randint(3, 8)} stresses per line ' \
        f'and the dominant meter should be {random.choice(meters)}.'
    rhymes = f'The poem\'s rhyme scheme will be {random.choice(rhyme_scheme)} requiring that the rhymes' \
        f'be, at least {random.choice(rhyme_types)}.'
    
    if rhyming:
        return lines + '\n' + stresses + '\n' + rhymes + '\n'
    else:
        return lines + '\n' + stresses + '\n'


def generate_museglob(markov_model: dict) -> str:
    return ''
        
  