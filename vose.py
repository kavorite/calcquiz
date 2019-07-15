from random import randint, random as randf

class Vose(object):
    def __init__(self, *dist):
        def drain(queue):
            if len(queue) > 0:
                yield queue.pop()
                yield from drain(queue)

        sigma = sum(dist)
        if sigma != 0:
            dist = tuple(x/sigma for x in dist)
        else:
            dist = tuple(1 for i in range(len(dist)))

        n = len(dist)
        m = 1/n
        small = []
        large = []
        push = lambda i, x: (small.append if x < m else large.append)(i)
        for i, x in enumerate(dist):
            push(i, x)

        self.prob = [0 for i in range(n)]
        self.alias = [0 for i in range(n)]
        for l, g in zip(drain(small), drain(large)):
            self.prob[l] = dist[l]*n
            self.alias[l] = g
            self.prob[g] = self.prob[g] + self.prob[l] - m
            push(g, dist[l] + dist[g] - m)
        for l in drain(large):
            self.prob[l] = 1
        for g in drain(small):
            self.prob[g] = 1

    def __iter__(self):
        return self

    def __next__(self):
        i = randint(0, len(self.prob)-1)
        return i if randf() < self.prob[i] else self.alias[i]


if __name__ == '__main__':
    from collections import Counter
    from itertools import islice
    dist = (1, 2, 3, 4, 5, 6)
    dice = Vose(*dist)
    iterc = int(1e6)
    want = {k: k*iterc/sum(dist) for k in dist}
    hist = Counter(islice(dice, iterc))
    error_counts = tuple(abs(hist[k]-want[k]) for k in want.keys())
    error = int(max(error_counts) / iterc * 100)
    print(f'{error}% error')

