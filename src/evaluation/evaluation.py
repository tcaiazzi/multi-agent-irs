from training import training_algorithm


def evaluate(algorithm_name: str, model_path: str):
    algorithm_class = getattr(training_algorithm, algorithm_name)
    config = algorithm_class("evaluation").config

    config['hiddens'] = []
    config['dueling'] = False

    # per l'evaluation
    config['evaluation_interval'] = 1

    algo = config.build()

    algo.restore(model_path)

    algo.evaluate()
