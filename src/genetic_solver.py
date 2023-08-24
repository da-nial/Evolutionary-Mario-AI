from random import uniform

from chromo import Chromo
from helper import generate_population, get_population_stats


class GeneticSolver:
    def __init__(self, game,
                 fitness_fn,
                 selection_fn,
                 reproduction_fn,
                 mutation_fn,
                 mutation_probability=0.2,
                 num_generations=500,
                 population_size=200,
                 convergence_epsilon=0.000001,
                 mutation_aggression=0.5
                 ):
        self.game = game

        self.fitness_fn = fitness_fn
        self.selection_fn = selection_fn
        self.reproduction_fn = reproduction_fn
        self.mutation_fn = mutation_fn

        self.num_generations = num_generations
        self.population_size = population_size
        self.convergence_epsilon = convergence_epsilon
        self.mutation_probability = mutation_probability
        self.mutation_aggression = mutation_aggression

    def run(self, level_idx):
        level = self.game.levels[level_idx]
        first_iteration_with_solution = None
        solution = None
        did_converge = False
        stats = []

        population = generate_population(self.population_size, level, self.fitness_fn)
        min_score, avg_score, max_score = get_population_stats(population)

        stats.append((min_score, avg_score, max_score))

        for i in range(self.num_generations):
            new_population = []

            for j in range(0, len(population), 2):
                x = self.selection_fn(population)
                y = self.selection_fn(population)

                new_childs_actions = self.reproduction_fn(x.actions, y.actions)
                for new_actions in new_childs_actions:
                    child = Chromo(level, new_actions, self.fitness_fn)

                    if uniform(0, 1) < self.mutation_probability:
                        self.mutation_fn(child, self.mutation_aggression)

                    new_population.append(child)

            for chromo in new_population:
                if chromo.fitness_criteria.max_steps == len(level):
                    first_iteration_with_solution = i
                    solution = chromo.actions
                    break

            new_min_score, new_avg_score, new_max_score = get_population_stats(new_population)
            stats.append((new_min_score, new_avg_score, new_max_score))

            did_converge = abs(new_avg_score - avg_score) < self.convergence_epsilon
            avg_score = new_avg_score
            population = new_population

            if solution is not None:
                break
            if did_converge:
                break

        return first_iteration_with_solution, solution, did_converge, stats

    def __str__(self):
        config = f"Fitness Function: {self.fitness_fn.__name__} | "
        config += f"Selection Function: {self.selection_fn.__name__}\n"
        config += f"Reproduction Function: {self.reproduction_fn.__name__} | "
        config += f"Mutation Function: {self.mutation_fn.__name__}\n"
        config += f"Mutation Probability: {self.mutation_probability} | "
        config += f"Num Generations: {self.num_generations}\n"
        config += f"Convergence Epsilon: {self.convergence_epsilon} | "
        config += f"Mutation Aggression: {self.mutation_aggression}"
        return config
