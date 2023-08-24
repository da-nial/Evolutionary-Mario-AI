class Chromo:
    def __init__(self, level, actions, fitness_fn):
        self.actions = actions
        self.fitness_criteria, self.fitness_score = fitness_fn(level, actions)
