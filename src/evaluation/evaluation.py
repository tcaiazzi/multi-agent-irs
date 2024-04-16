from training import training_algorithm


def evaluate(algorithm_name: str, model_path: str, num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int,
                 k_def: float):
    algorithm_class = getattr(training_algorithm, algorithm_name)
    config = algorithm_class("evaluation", num_agents, num_att_actions, k_att, num_def_actions, k_def).config

    config['hiddens'] = []
    config['dueling'] = False

    # per l'evaluation
    config['evaluation_interval'] = 1

    algo = config.build()

    algo.restore(model_path)

    algo.evaluate()
