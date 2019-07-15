from random import randint, random as randf
from collections import Counter, deque
from vose import Vose

class CMA(object):
    def __init__(self):
        self._n = 0
        self._value = 0

    def update(self, x):
        self._n += 1
        self._value = ((self._n-1)*self._value + x) / self._n
    
    def value(self):
        return self._value


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



smappings = {''.join(ans.lower().split()): prompt
             for prompt, ans in mappings.items()}


def check(prompt, ans):
    k = ''.join(ans.lower().split())
    if k not in smappings:
        return False
    return smappings[k] == prompt


prompts = tuple()
accuracy = [CMA() for i in range(len(mappings))]
while True:
    if len(prompts) == 0:
        dice = Vose(*(cma.value() for cma in accuracy))
        prompts = tuple(mappings.keys())
        round_accuracy = CMA()
        n = 0

    i = next(dice)
    prompt = prompts[i]
    ans = input(f'{prompt} = ')
    n += 1
    if check(prompt, ans):
        prompts = tuple(prompts[:i]+prompts[i+1:])
        completion = int(100 * (1 - (len(prompts) / len(mappings))))
        accuracy[i].update(1)
        round_accuracy.update(1)
        prn_accuracy = int(round_accuracy.value() * 100)
        print(f'correct (round {prn_accuracy}% accurate; {completion}% complete)')
    else:
        accuracy[i].update(0)
        round_accuracy.update(0)
        print(mappings[prompt])
