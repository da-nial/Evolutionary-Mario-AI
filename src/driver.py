from os.path import join

from fitness import fitness_fn_with_winning, fitness_fn_without_winning
from game import Game
from genetic_solver import GeneticSolver
from helper import load_levels, weighted_select, half_select, single_point_crossover, two_point_crossover, unbiased_mutate
from stats import plot


def main():
    # levels = ["____G__L__", "___G_M___L_"]
    input_dir = "./levels"
    output_dir = "./output"
    levels = load_levels(_dir=input_dir)

    game = Game(levels)

    # print(levels[1])
    # chromo = Chromo("_G___", "02211", fitness_fn_with_winning)
    # print(chromo.fitness_criteria.max_steps)
    # print(chromo.fitness_criteria.did_win)
    # exit()

    solver = GeneticSolver(game,
                           fitness_fn_with_winning,
                           half_select,
                           single_point_crossover,
                           unbiased_mutate,
                           population_size=200,
                           mutation_probability=0.1,
                           )

    # solver = GeneticSolver(game,
    #                        fitness_fn_without_winning,
    #                        weighted_select,
    #                        two_point_crossover,
    #                        unbiased_mutate,
    #                        population_size=500,
    #                        mutation_probability=0.5
    #                        )

    for level_idx in range(6, 7):
        first_generation_with_solution, solution, did_converge, stats = solver.run(level_idx)

        plot_text = solver.__str__()
        plot_text += "\n"
        plot_text += f"Convergence: {did_converge}, "
        plot_text += f"First Generation with Solution: {first_generation_with_solution}\n"
        plot_text += f"Solution: {solution}"

        print(plot_text)
        plot(stats, plot_text, join(output_dir, "level" + str(level_idx) + ".png"))
        print(f"plotted results of level {level_idx} successfully!\n\n")


if __name__ == '__main__':
    main()
