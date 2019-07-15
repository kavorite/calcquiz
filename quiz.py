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


prompts = tuple(mappings.keys())
accuracy = [CMA() for i in range(len(mappings))]
total_accuracy = CMA()
while True:
    dice = Vose(*(1-cma.value() for cma in accuracy))
    i = next(dice)
    prompt = prompts[i]
    ans = input(f'{prompt} = ')
    if check(prompt, ans):
        completion = int(100 * (1 - (len(prompts) / len(mappings))))
        accuracy[i].update(1)
        total_accuracy.update(1)
        prn_accuracy = int(total_accuracy.value() * 100)
        print(f'correct ({prn_accuracy}% accurate)')
    else:
        accuracy[i].update(0)
        total_accuracy.update(0)
        print(mappings[prompt])
