__author__ = 'Romer Ibo'

from math import floor, ceil
from random import shuffle, randrange, choice
from itertools import product
from forest_objects import Tree, Lumberjack, Bear


class Forest:
    def __init__(self, forest_size, tree_init_percentage, lumberjack_init_percentage, bear_init_percentage,
                 base_percentage, tree_init_age_min, tree_init_age_max, tree_age_limit, sapling_age_limit,
                 tree_spawn_rate, elder_tree_spawn_rate):
        self.size = forest_size
        self.possible_spots = list(product(range(self.size), range(self.size)))
        self.time = 0
        self.trees = dict()
        self.lumberjacks = dict()
        self.bears = dict()
        self.change = dict(new_saplings=0, new_trees=0, new_elder_trees=0, month_harvested=0, year_harvested=0,
                           month_mawed=0, year_mawed=0)
        self.tree_age_limit = tree_age_limit
        self.sapling_age_limit = sapling_age_limit
        self.base_percentage = base_percentage
        self.tree_spawn_rate = tree_spawn_rate
        self.elder_tree_spawn_rate = elder_tree_spawn_rate
        tree_init_count = floor((forest_size ** 2) * tree_init_percentage / base_percentage)
        lumberjack_init_count = ceil((forest_size ** 2) * lumberjack_init_percentage / base_percentage)
        bear_init_count = floor((forest_size ** 2) * bear_init_percentage / base_percentage)
        print("Trees: {}, Lumberjacks: {}, Bears: {}".format(tree_init_count, lumberjack_init_count, bear_init_count))
        coords = list(product(range(self.size), range(self.size)))
        shuffle(coords)
        for spot in coords[:lumberjack_init_count]:
            self.lumberjacks[spot] = Lumberjack()

        coords = coords[lumberjack_init_count:]
        shuffle(coords)
        for spot in coords[:tree_init_count]:
            self.trees[spot] = Tree(tree_init_age_min, tree_init_age_max)

        shuffle(coords)
        for spot in coords[:bear_init_count]:
            self.bears[spot] = Bear(0)

    # Creates a shuffled list of valid movement spots at the length of possible movement attempts
    def new_spot_list(self, location, attempts):
        next_spot = list(product(range(location[0]-1, location[0]+2), range(location[1]-1, location[1]+2)))
        next_spot.pop(4)
        shuffle(next_spot)
        selected = list()
        for i in range(0, len(next_spot)):
            if -1 < next_spot[i][0] < self.size and -1 < next_spot[i][1] < self.size:
                selected.append(next_spot[i])
            if len(selected) >= attempts:
                break
        return selected

    # moves objects in a list to a new location
    def move_objects(self, move_list):
        for current_object in move_list:
            object_type = current_object[1]
            current_location = current_object[0]
            if object_type == 'Lumberjack' and current_location in self.lumberjacks:
                original_location = current_object[0]
                temp_lumberjack = self.lumberjacks.pop(current_location)
                for x in range(0, 2):
                    for possible_spot in self.new_spot_list(current_location, 2):
                        if possible_spot not in self.lumberjacks:
                            current_location = possible_spot
                            break
                    if current_location == original_location or current_location in self.bears:
                        break
                    original_location = current_location
                if current_location not in self.bears:
                    self.lumberjacks[current_location] = temp_lumberjack
                if current_location in self.trees:
                    tree_age = self.trees[current_location].get_age()
                    if tree_age >= self.tree_age_limit:
                        self.trees.pop(current_location)
                        self.change['year_harvested'] += 2
                        self.change['month_harvested'] += 2
                    elif tree_age >= self.sapling_age_limit:
                        self.trees.pop(current_location)
                        self.change['year_harvested'] += 1
                        self.change['month_harvested'] += 1
            elif object_type == 'Bear'and current_location in self.bears:
                original_location = current_object[0]
                temp_bears = self.bears.pop(current_location)
                for x in range(0, 5):
                    for possible_spot in self.new_spot_list(current_location, 2):
                        if possible_spot not in self.bears:
                            current_location = possible_spot
                            break
                    if current_location == original_location or current_location in self.trees:
                        break
                    original_location = current_location
                self.bears[current_location] = temp_bears
                if current_location in self.lumberjacks:
                    self.lumberjacks.pop(current_location)
                    self.change['month_mawed'] += 1
                    self.change['year_mawed'] += 1
        if self.change['month_harvested'] > 0:
            print("Month [{:0>4}]: [{}] pieces of lumber harvested by Lumberjacks.".format(
                self.time, self.change['month_harvested']))
            self.change['month_harvested'] = 0
        if self.change['month_mawed'] > 0:
            print("Month [{:0>4}]: [{}] Lumberjack was Maw'd by a bear.".format(self.time, self.change['month_mawed']))
            self.change['month_mawed'] = 0

    # prints out required yearly updates
    def yearly_update(self, update_list):
        for _ in update_list:
            print("yearly object update [not used]")
        if self.change['year_mawed'] > 0:
            self.bears.pop(choice(list(self.bears.keys())))
            self.change['year_mawed'] = 0
            print("Year [{:0>3}]: {} Bear captured by Zoo.".format(int(self.time/12), 1))
        else:
            shuffle(self.possible_spots)
            for test_new_spot in self.possible_spots:
                if test_new_spot not in self.bears:
                    self.bears[test_new_spot] = Bear(0)
                    print("Year [{:0>3}]: {} new Bear added.".format(int(self.time/12), 1))
                    break
        if self.change['year_harvested'] < len(self.lumberjacks):
            self.lumberjacks.pop(choice(list(self.lumberjacks.keys())))
            print("Year [{:0>3}]: {} Pieces of lumber harvested {} new Lumberjacks fired.".format(
                int(self.time/12), self.change['year_harvested'], 1
            ))
            self.change['year_harvested'] = 0
        else:
            shuffle(self.possible_spots)
            hire_count = int(((self.change['year_harvested']-len(self.lumberjacks))/10)+1)
            for test_new_spot in self.possible_spots:
                if hire_count <= 0:
                    break
                if test_new_spot not in self.lumberjacks:
                    self.lumberjacks[test_new_spot] = Lumberjack()
                    hire_count -= 1
            print("Year [{:0>3}]: {} Pieces of lumber harvested {} new Lumberjacks hired.".format(
                int(self.time/12), self.change['year_harvested'],
                int((self.change['year_harvested']-len(self.lumberjacks))/10-hire_count)
            ))
            self.change['year_harvested'] = 0

    # prints out required monthly updates
    def monthly_update(self, update_list):
        size = len(self.trees)
        for current_object in update_list:
            object_type = current_object[1]
            current_location = current_object[0]
            if object_type == 'Tree' and current_location in self.trees:
                tree_age = self.trees[current_location].get_age()
                if tree_age >= self.tree_age_limit and self.elder_tree_spawn_rate <= randrange(0, self.base_percentage):
                    for possible_spot in self.new_spot_list(current_location, 8):
                        if possible_spot not in self.trees:
                            self.trees[possible_spot] = Tree(0, 1)
                            break
                elif tree_age >= self.sapling_age_limit and self.tree_spawn_rate <= randrange(0, self.base_percentage):
                    for possible_spot in self.new_spot_list(current_location, 8):
                        if possible_spot not in self.trees:
                            self.trees[possible_spot] = Tree(0, 1)
                            break
        size = len(self.trees) - size
        if size > 0:
            print("Month [{:0>4}]: [{}] new Saplings Created.".format(self.time, size))

    # updates all of the objects in forest (currently only updating tree ages and tree types)
    def update_objects(self):
        for tree_key in self.trees.keys():
            self.trees[tree_key].update_age()
            if self.trees[tree_key].get_age() == self.tree_age_limit:
                self.change['new_trees'] += 1
            elif self.trees[tree_key].get_age() == self.elder_tree_spawn_rate:
                self.change['new_elder_trees'] += 1

    # conducts month simulation and update of a forest
    def action(self):
        lumberjacks_list = list([(key, self.lumberjacks[key].__class__.__name__) for key in self.lumberjacks.keys()])

        bears_list = list([(key, self.bears[key].__class__.__name__) for key in self.bears.keys()])
        self.time += 1

        move_list = lumberjacks_list + bears_list
        shuffle(move_list)
        Forest.move_objects(self, move_list)

        tree_list = list([(key, self.trees[key].__class__.__name__) for key in self.trees.keys()])

        month_update_list = tree_list
        shuffle(month_update_list)

        Forest.monthly_update(self, month_update_list)

        if self.time % 12 == 0:
            Forest.yearly_update(self, list())

        Forest.update_objects(self)
        self.print_forest()

    # returns forest simulation time
    def get_time(self):
        return self.time

    # prints out properties of the forest
    def print_forest(self):
        if self.time % 12 == 0:
            saplings = 0
            trees = 0
            elders = 0
            for look in self.trees.values():
                age = look.get_age()
                if age >= self.tree_age_limit:
                    elders += 1
                elif age >= self.sapling_age_limit:
                    trees += 1
                else:
                    saplings += 1
            print("Year [{:0>3}]: Forest has {} Trees, {} Saplings, {} Elder Tree, {} Lumberjacks and {} Bears."
                  .format(int(self.time/12), trees, saplings, elders, len(self.lumberjacks), len(self.bears)))