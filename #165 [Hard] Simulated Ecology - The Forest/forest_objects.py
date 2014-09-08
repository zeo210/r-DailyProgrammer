__author__ = 'Romer Ibo'


from random import randrange
from itertools import product


alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Generator used to give each forest object a unique ID
def id_generator():
    i = 1
    while True:
        for p in product(alphabet, repeat=i):
            yield ''.join(p)
        i += 1

# Tree object for forest
class Tree:
    next_id = id_generator()

    def __init__(self, min_age, max_age):
        self.age = randrange(min_age, max_age)  # age calculated in months
        self.id = "T{}".format(next(Tree.next_id))

    def update_age(self):
        self.age += 1

    def get_age(self):
        return self.age

    def match_id(self, id_in):
        return id_in == self.id

# Lumberjack object for forest
class Lumberjack:
    next_id = id_generator()

    def __init__(self):
        self.collected = 0  # number of lumber collected. Not required for challenge
        self.id = "L{}".format(next(Lumberjack.next_id))

    def match_id(self, id_in):
        return id_in == self.id

# Bear object for forest
class Bear:
    next_id = id_generator()

    def __init__(self, age):
        self.age = age  # age calculated in months. Not required for challenge
        self.id = "B{}".format(next(Bear.next_id))

    def match_id(self, id_in):
        return id_in == self.id
