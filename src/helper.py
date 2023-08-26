from os.path import join
from random import randint, choice, choices

from tabulate import tabulate

from chromo import Chromo


def print_table(data_dict):
    table_data = [(key, value) for key, value in data_dict.items()]
    table = tabulate(table_data, headers=["Attribute", "Value"], tablefmt="grid")
    print(table)


def read_from_file(path):
    with open(path, 'r') as f:
        return f.readline()


def load_levels(_dir="./levels"):
    levels = []
    for i in range(1, 11):
        name = "level" + str(i) + ".txt"
        level_i = read_from_file(join(_dir, name))
        levels.append(level_i)

    return levels


def generate_population(population_size, level, fitness_fn):
    chromo_len = len(level)

    population = []
    for _ in range(population_size):
        actions = ''.join([choice(['0', '1', '2']) for _ in range(chromo_len)])
        actions = remove_double_jump(actions)

        new_chromo = Chromo(level, actions, fitness_fn)
        population.append(new_chromo)

    return population


def remove_double_jump(actions):
    actions_ls = list(actions)
    for i in range(len(actions_ls) - 1):
        if actions_ls[i] == '1' and actions_ls[i + 1] == '1':
            offset = randint(0, 1)
            actions_ls[i + offset] = choice(['0', '2'])

    return ''.join(actions_ls)


def get_population_stats(population):
    population_score = [chromo.fitness_score for chromo in population]
    avg_score = sum(population_score) / len(population)
    min_score = min([chromo.fitness_score for chromo in population])
    max_score = max([chromo.fitness_score for chromo in population])

    return min_score, avg_score, max_score


def weighted_select(population):
    scores = [chromo.fitness_score for chromo in population]
    weights = [float(score) / sum(scores) for score in scores]
    selected_chromo = choices(population=population, weights=weights, k=1)[0]

    return selected_chromo


def half_select(population):
    population.sort(key=lambda chromo: chromo.fitness_score)
    selected_chromo = choice(population[len(population) // 2:])
    return selected_chromo


def single_point_crossover(actions_x, actions_y):
    n = len(actions_x)
    c = randint(0, n)

    child_1_actions = actions_x[:c] + actions_y[c:]
    child_2_actions = actions_x[:c] + actions_y[c:]
    return [child_1_actions, child_2_actions]


def two_point_crossover(actions_x, actions_y):
    n = len(actions_x)

    c1 = randint(0, n)
    c2 = randint(0, n)

    if c1 > c2:
        hold = c1
        c1 = c2
        c2 = hold

    child_1_actions = actions_x[:c1] + actions_y[c1:c2] + actions_x[c2:]
    child_2_actions = actions_y[:c1] + actions_x[c1:c2] + actions_y[c2:]

    return [child_1_actions, child_2_actions]


def unbiased_mutate(chromo, aggression):
    actions = list(chromo.actions)
    n = len(actions)

    # if not chromo.fitness_criteria.did_jump_in_last:
    #     actions[-1] = '1'

    num_changing_actions = int(n * aggression)
    for _ in range(num_changing_actions):
        idx = choice(range(n))
        domain = ['0', '1', '2']
        domain.remove(actions[idx])
        actions[idx] = choice(domain)

    chromo.actions = "".join(actions)


def biased_mutate(chromo, aggression):
    pass
