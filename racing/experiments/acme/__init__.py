from functools import partial
from typing import Optional

from racing.algorithms import make_mpo_agent
from racing.algorithms.d4pg import make_d4pg_agent
from racing.experiments.acme.experiment import SingleAgentExperiment
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

from racing.experiments.util import read_hyperparams


def choose_agent(name: str, param_file: Optional[str], checkpoint_path: str):
    params = read_hyperparams(param_file) if param_file else {}
    print(params.keys())
    if name == 'mpo':
        constructor = partial(make_mpo_agent, hyperparams=params, checkpoint_path=checkpoint_path)
    elif name == 'd4pg':
        constructor = partial(make_d4pg_agent, hyperparams=params, checkpoint_path=checkpoint_path)
    else:
        raise NotImplementedError(name)
    return constructor

def make_experiment(args, logdir):
    checkpoint_path = f'{logdir}/checkpoints'
    env_config = SingleAgentExperiment.EnvConfig(
        track=args.track,
        task=args.task,
        action_repeat=args.action_repeat,
        training_time_limit=args.training_time_limit,
        eval_time_limit=args.eval_time_limit
    )
    experiment = SingleAgentExperiment(env_config=env_config, seed=args.seed, logdir=logdir)
    agent_ctor = choose_agent(name=args.agent, param_file=args.params, checkpoint_path=checkpoint_path)
    return experiment, agent_ctor