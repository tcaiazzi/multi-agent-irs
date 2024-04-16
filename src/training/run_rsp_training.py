# se lancio dalla cartella principale
import os.path
import sys

sys.path.append('./')

from ray import train, tune
from ray.rllib.utils.framework import try_import_torch
# SERVE PER AVERE LO SPAZIO DELLE AZIONI DI DIMENSIONI DIVERSE
# e VOLENDO ANCHE LE OBSERVATIONs

from training import training_algorithm
from visualizzazione import visualizza_reward_mosse

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


def run_rsp_training(algorithm: str, training_iteration: int, gamma: float,
                     num_agents: int, num_att_actions: int, k_att: float, num_def_actions: int, k_def: float):

    torch, nn = try_import_torch()
    torch.cuda.empty_cache()

    # COndizioni di stopping degli algoritmi
    stop = {
        # epoche/passi dopo le quali il training si arresta
        "training_iteration": training_iteration,

        # "timesteps_total":2,

        # passi ambientali dell'agente nell'ambiente
        # ci sarebbe un minimo di 200
        # "timesteps_total": 2,

        # ferma il training quando la ricompensa media dell'agente nell'episodio è pari o maggiore
        # "episode_reward_max": 5,
    }

    # RAY  VIENE UTILIZZATO PER POTER FARE IL TUNING DEGLI IPERPARAMETRI
    # SI PUO DEFINIRE UN RANGE ED IN AUTOMATICA FA I DIVERSI TRAINING CON LE DIVERSE CONFIG
    # ray.shutdown()
    # ray.init()

    algorithm_class = getattr(training_algorithm, algorithm)

    config = algorithm_class("training", num_agents, num_att_actions, k_att, num_def_actions, k_def).config

    # Mi risolve i problemi di mismatch con la rete, non so perche, ma per l'action mask
    config['hiddens'] = []
    config['dueling'] = False

    # per l'evaluation
    config['evaluation_interval'] = 1

    algo = config.training(gamma=gamma).build()

    result_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
    os.makedirs(result_path, exist_ok=True)

    results = tune.Tuner(
        algorithm_to_trainable[algorithm],
        run_config=train.RunConfig(stop=stop, verbose=1, storage_path=result_path),
        param_space=config,
    ).fit()

if __name__ == '__main__':
    run_rsp_training(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]))
