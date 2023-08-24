class Fitness:
    def __init__(self,
                 did_win,
                 max_steps,
                 did_jump_in_last,
                 total_mushrooms_eaten,
                 total_poinless_moves,
                 total_goompas_killed):
        self.did_win = did_win
        self.max_steps = max_steps
        self.did_jump_in_last = did_jump_in_last
        self.total_mushrooms_eaten = total_mushrooms_eaten
        self.total_poinless_moves = total_poinless_moves
        self.total_goompas_killed = total_goompas_killed


def fitness_fn_with_winning(level, actions):
    weights = {
        'winning_score': 5,
        'step_score': 1,
        'eating_mushroom_score': 2,
        'jumping_in_last_score': 1,
        'killing_goompa_score': 2,
        'pointless_move_score': -0.5
    }
    fitness = fitness_fn(level, actions)

    return fitness, get_fitness_score(weights, fitness, check_win=True)


def fitness_fn_without_winning(level, actions):
    weights = {
        'winning_score': 5,
        'step_score': 1,
        'eating_mushroom_score': 2,
        'jumping_in_last_score': 1,
        'killing_goompa_score': 2,
        'pointless_move_score': -0.5
    }

    fitness = fitness_fn(level, actions)
    return fitness, get_fitness_score(weights, fitness, check_win=False)


def fitness_fn(level, actions):
    max_steps = 0
    total_mushrooms_eaten = 0
    total_pointless_moves = 0  # useless jumps OR DODGES!
    total_goompas_killed = 0

    i = 0
    while i < len(level):
        j, steps, num_mushrooms_eaten, num_pointless_moves, num_goompas_killed = _fitness_fn(level, actions, i)
        total_mushrooms_eaten += num_mushrooms_eaten
        total_pointless_moves += num_pointless_moves
        total_goompas_killed += num_goompas_killed
        if steps > max_steps:
            max_steps = steps
        i = j

    did_win = max_steps == len(level)
    did_jump_in_last = actions[-1] == '1'
    fitness = Fitness(did_win,
                      max_steps,
                      did_jump_in_last,
                      total_mushrooms_eaten,
                      total_pointless_moves,
                      total_goompas_killed)

    return fitness


def _fitness_fn(level, actions, start):
    steps = 0
    num_mushrooms_eaten = 0
    num_pointless_moves = 0  # useless jumps OR DODGES!
    num_goompas_killed = 0

    j = start
    is_action_valid = True
    while is_action_valid and j < len(level):
        current_step = level[j]
        is_action_valid = False

        if current_step == '_':
            is_action_valid = True
            if actions[j - 1] != '0':
                num_pointless_moves += 1

        elif current_step == 'G':
            if actions[j - 1] == '1':
                is_action_valid = True
            elif j - 2 > 0 and actions[j - 2] == '1':
                is_action_valid = True
                num_goompas_killed += 1

        elif current_step == 'L':
            if actions[j - 1] == '2':
                is_action_valid = True

        elif current_step == 'M':
            is_action_valid = True
            if actions[j - 1] != '1':
                num_mushrooms_eaten += 1

        j += 1
        steps += 1

    return j, steps, num_mushrooms_eaten, num_pointless_moves, num_goompas_killed


def get_fitness_score(weights, fitness, check_win=True):
    score = 0
    if fitness.did_jump_in_last:
        score += weights["jumping_in_last_score"]

    score += fitness.max_steps * weights["step_score"]
    score += fitness.total_mushrooms_eaten * weights["eating_mushroom_score"]
    score += fitness.total_poinless_moves * weights["pointless_move_score"]
    score += fitness.total_goompas_killed * weights["killing_goompa_score"]

    if check_win:
        if fitness.did_win:
            score += weights["winning_score"]

    return score
