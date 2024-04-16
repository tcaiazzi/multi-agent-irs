# Multi Agent IRS

## Pre-Requisites
```bash
python3 -m pip install -r requirements.txt
python3 -m pip install ray[train]
```

## Training

To train a model using a specific algorithm, go inside the `src` directory, then:
```bash
python3 train.py --algorithm DQN --epoch 10 --gamma 0.9 
```

Possible algorithms include: 
- `DQN`
- `ApexDQN`
- `PPO`
- `PG`
- `Impala`

The resultant models, will be put inside the `models` directory in the project root. 

## Evaluate