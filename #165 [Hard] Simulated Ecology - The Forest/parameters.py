__author__ = 'Romer Ibo'

import sys
import argparse

default_sapling_age_limit = 12
default_tree_age_limit = 120
default_tree_spawn_rate = 10
default_elder_tree_spawn_rate = 20

default_simulation_time = 4800
default_forest_size = 5

default_tree_init_percentage = 50
default_lumberjack_init_percentage = 10
default_bear_init_percentage = 2

default_tree_to_lumber = 1
default_elder_tree_to_lumber = 2

default_base_percentage = 100

default_tree_init_age_min = 12
default_tree_init_age_max = 120

default_BTL_graph = False

# Establishes arguments, collects possible values, checks if arguments are valid, and returns values
def parameter_check():
    parser = argparse.ArgumentParser(description='Enter any optional parameters')
    parser.add_argument('-sal', '--sapling_age_limit',
                        type=int,
                        action='store',
                        default=default_sapling_age_limit,
                        help='Age Saplings grow to Trees. Default = {}'
                        .format(default_sapling_age_limit))
    parser.add_argument('-tal', '--tree_age_limit',
                        type=int,
                        action='store',
                        default=default_tree_age_limit,
                        help='Age Trees grow to Elder Trees. Default = {}'
                        .format(default_tree_age_limit))
    parser.add_argument('-tsr', '--tree_spawn_rate',
                        type=int,
                        action='store',
                        default=default_tree_spawn_rate,
                        help='Rate Trees spawn Saplings. Default = {}'
                        .format(default_tree_spawn_rate))
    parser.add_argument('-etsr', '--elder_tree_spawn_rate',
                        type=int,
                        action='store',
                        default=default_elder_tree_spawn_rate,
                        help='Rate Elder Trees spawn Saplings. Default = {}'
                        .format(default_elder_tree_spawn_rate))
    parser.add_argument('-st', '--simulation_time',
                        type=int,
                        action='store',
                        default=default_simulation_time,
                        help='Number of months simulation runs for. Default = {}'
                        .format(default_simulation_time))
    parser.add_argument('-fs', '--forest_size',
                        type=int,
                        action='store',
                        default=default_forest_size,
                        help='Custom size of forest. Default = {}'
                        .format(default_forest_size))
    parser.add_argument('-tip', '--tree_init_percentage',
                        type=int,
                        action='store',
                        default=default_tree_init_percentage,
                        help='Percentage of forest initialized with Trees. Default = {}'
                        .format(default_tree_init_percentage))
    parser.add_argument('-lip', '--lumberjack_init_percentage',
                        type=int,
                        action='store',
                        default=default_lumberjack_init_percentage,
                        help='Percentage of forest initialized with Lumberjacks. Default = {}'
                        .format(default_lumberjack_init_percentage))
    parser.add_argument('-bip', '--bear_init_percentage',
                        type=int,
                        action='store',
                        default=default_bear_init_percentage,
                        help='Percentage of forest initialized with Bears. Default = {}'
                        .format(default_bear_init_percentage))
    parser.add_argument('-bp', '--base_percentage',
                        type=int,
                        action='store',
                        default=default_base_percentage,
                        help='Denominator value for percentage parameters. Default = {}'
                        .format(default_bear_init_percentage))
    parser.add_argument('-tiamin', '--tree_init_age_min',
                        type=int,
                        action='store',
                        default=default_tree_init_age_min,
                        help='Minimum age of init Trees (inclusive). Default = {}'
                        .format(default_tree_init_age_min))
    parser.add_argument('-tiamax', '--tree_init_age_max',
                        type=int,
                        action='store',
                        default=default_tree_init_age_max,
                        help='Maximum age of init Trees (exclusive). Default = {}'
                        .format(default_tree_init_age_max))
    args = parser.parse_args()
    print(args)

    if args.sapling_age_limit >= args.tree_age_limit:
        print("Saplings age limit is greater than or equal to Tree age limit, check parameters",
              file=sys.stderr)
        exit(1)
    if args.tree_spawn_rate > args.base_percentage:
        print("Trees spawn Saplings rate is greater than 100%, check parameters",
              file=sys.stderr)
        exit(1)
    if args.elder_tree_spawn_rate > args.base_percentage:
        print("Elder Trees spawn Saplings rate is greater than 100%, check parameters",
              file=sys.stderr)
        exit(1)
    if args.tree_init_percentage + args.lumberjack_init_percentage > args.base_percentage:
        print("Sum of initialization percentages of tree and lumberjacks is larger than base percentage, "
              "check parameters",
              file=sys.stderr)
        exit(1)
    if args.lumberjack_init_percentage + args.bear_init_percentage > args.base_percentage:
        print("Sum of initialization percentages of lumberjacks and bears is larger than base percentage, "
              "check parameters",
              file=sys.stderr)
        exit(1)
    if args.tree_init_age_min > args.tree_init_age_max:
        print("Minimum Tree age is greater than maximum tree age, check parameters",
              file=sys.stderr)
        exit(1)

    return args