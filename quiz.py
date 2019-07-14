from random import randint
from collections import Counter
import re

mappings = {
        '∫tan(u) du': 'ln|sec(u)| + C',
        '∫cot(u) du': 'ln|sin(u)| + C',
        '∫csc(u) du': 'ln|csc(u) - cot(u)| + C',
        '∫sec(u) du': 'ln|sec(u) + tan(u)| + C',
        '∫csc(u) cot(u) du': '-csc(u) + C',
        '∫csc²(u) du': '-cot(u) + C',
        '∫sec²(u) du': 'tan(u) + C',
        '∫sin²(u) du': '1/2 - 1/2 cos(2u) + C',
        '∫cos²(u) du': '1/2 + 1/2 cos(2u) + C',
        '∫du / (a²+u²)': '1/a arctan(u/a) + C',
        '∫du / √(a²+u²)': 'arcsin(u/a) + C',
        '∫cos(u) du': 'sin(u) + C',
        '∫sin(u) du': '-cos(u) + C',
        '∫aᵘ du': 'a^u / ln(a) + C'
}


def tokenize(s):
    return tuple(re.findall(r'\w+', s))


smappings = {tokenize(ans.lower()): prompt
             for prompt, ans in mappings.items()}


def check(prompt, ans):
    k = tokenize(ans.lower())
    if k not in smappings:
        return False
    return smappings[k] == prompt


prompts = tuple()
promptc = 0
accuracy = 0
while True:
    if len(prompts) == 0:
        prompts = tuple(mappings.keys())
        correct = set()
        accuracy = 0

    i = randint(0, len(prompts)-1)
    prompt = prompts[i]
    ans = input(f'{prompt} = ')
    promptc += 1
    if check(prompt, ans):
        correct.add(prompt)
        prompts = tuple(prompts[:i]+prompts[i+1:])
        completion = int(100 * (1 - (len(prompts) / len(mappings))))
        accuracy = ((promptc-1)*accuracy + 1) / promptc
        prn_accuracy = int(100 * accuracy)
        print(f'correct (round {prn_accuracy}% accurate; {completion}% complete)')
    else:
        accuracy = ((promptc-1)*accuracy) / promptc
        print(mappings[prompt])
