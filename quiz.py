from random import randint

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
while True:
    if len(prompts) == 0:
        i = randint(0, len(mappings)-1)
        prompts = tuple(mappings.keys())
        accuracy = 0
        n = 0

    i = randint(0, len(prompts)-1)
    prompt = prompts[i]
    ans = input(f'{prompt} = ')
    n += 1
    if check(prompt, ans):
        prompts = tuple(prompts[:i]+prompts[i+1:])
        completion = int(100 * (1 - (len(prompts) / len(mappings))))
        accuracy = ((n-1)*accuracy + 1) / n
        prn_accuracy = int(100 * accuracy)
        print(f'correct (round {prn_accuracy}% accurate; {completion}% complete)')
    else:
        accuracy = ((n-1)*accuracy) / n
        print(mappings[prompt])
