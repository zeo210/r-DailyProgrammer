__author__ = 'Romer Ibo'
#file used for me to test ideas for the project (this file is not used with the main program)

from itertools import product
from random import shuffle

test_dict = {(0, 0): "hello world", (1, 4): "test1", (6, 2): "test2"}

alphabet = "abcdefghijklmnopqrstuvwxyz"

print(test_dict)

def id_generator():
    i = 1
    while i < 4:
        for p in product(alphabet, repeat=i):
            yield ''.join(p)
        i += 1


def spot_generator(location, max, attempts):
    next_spot = list(product(range(location[0]-1, location[0]+2), range(location[1]-1, location[1]+2)))
    next_spot.pop(4)
    print(next_spot[:max])
    shuffle(next_spot)
    for i in range(0, max):
        if -1 < next_spot[i][0] < max and -1 < next_spot[i][1] < max:
            yield next_spot[i]

print(spot_generator((3, 5), 6, 2))

for key in test_dict.keys():
    print(key)

print('abc' * 7)