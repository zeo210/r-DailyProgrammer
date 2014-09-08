__author__ = 'Romer Ibo'

from parameters import parameter_check
from forest import Forest

# Main function to run forest simulation
def main():
    args = parameter_check()
    forest = Forest(args.forest_size, args.tree_init_percentage, args.lumberjack_init_percentage,
                    args.bear_init_percentage, args.base_percentage, args.tree_init_age_min, args.tree_init_age_max,
                    args.tree_age_limit, args.sapling_age_limit, args.tree_spawn_rate, args.elder_tree_spawn_rate)
    for x in range(0, 4800):
        forest.action()
        if len(forest.trees) == 0:
            print("Simulation Halt: no more trees exist")
            break

if __name__ == '__main__':
    main()