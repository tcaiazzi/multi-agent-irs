# se lancio dalla cartella principale
import os.path
import sys

sys.path.append('./')

from ray import train, tune
from ray.rllib.utils.framework import try_import_torch

from training import training_configurations

# NEI RESULT TROVIAMO:
# episode_length NUMERO DEI TURNI PRIMA DELLA TERMINAZIONE (1 SOLO ATTACCANTE, 2 ATTACCANTE+DIFENSORE ...)
# policy_*_reward METTE SOLO LE REWARD OTTENUTE DALL'AGENTE QUANDO VINCE
# episode_reward È LA SOMMA DELLE REWARD ATTACCANTE E DIFENSORE (AD OGNI TURNO NE VINCE UNO SOLO)
# MI SON FATTO UN RESULT TUTTO MIO CUSTOM, PER ORA SCRIVE SUL FILE MA MODIFICABILE

algorithm_to_trainable = {
    "DQN": "DQN",
    "ApexDQN": "Apex",
    "PPO": "PPO",
    "PG": "PG",
    "Impala": "IMPALA"
}


def run_training(algorithm: str, training_iteration: int, gamma: float,
                 num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int, k_def: float):
    torch, nn = try_import_torch()
    torch.cuda.empty_cache()

    # Algorithm stop conditions
    stop = {
        "training_iteration": training_iteration,
        # "timesteps_total":2,
        # "episode_reward_max": 5, # Stop training if the reward is >= to the value
    }

    algorithm_class = getattr(training_configurations, f"{algorithm}Configuration")

    config = algorithm_class("training", num_agents, num_att_actions, k_att, num_def_actions, k_def).config

    print(dir(config))
    # exit()

    config['hiddens'] = []
    config['dueling'] = False

    # per l'evaluation
    config['evaluation_interval'] = 1
    config.training(gamma=gamma).build()

    result_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    os.makedirs(result_path, exist_ok=True)

    tune.Tuner(
        algorithm_to_trainable[algorithm],
        run_config=train.RunConfig(stop=stop, verbose=1, storage_path=result_path),
        param_space=config,
    ).fit()
