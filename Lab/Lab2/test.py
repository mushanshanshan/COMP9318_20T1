import itertools

s = ['a', 'all','b','all']

for n in itertools.combinations(s, 2):
    print(n)