#!/bin/bash

if [ "$1" = "-e" ]; then
	if [ "$2" = "PG" ]; then
		clear && python3 ./evaluate/evaluationPG.py
	fi
	if [ "$2" = "PPO" ]; then
		clear && python3 ./evaluate/evaluationPPO.py
	fi
	if [ "$2" = "DQN" ]; then
		clear && python3 ./evaluate/evaluationDQN.py
	fi
	if [ "$2" = "ApexDQN" ]; then
		clear && python3 ./evaluate/evaluationApexDQN.py
	fi
	if [ "$2" = "Impala" ]; then
		clear && python3 ./evaluate/evaluationImpala.py
	fi
else
	if [ "$1" = "PG" ]; then
		clear && python3 ./training/run_rspPG.py
	fi
	if [ "$1" = "PPO" ]; then
		clear && python3 ./training/run_rspPPO.py
	fi
	if [ "$1" = "DQN" ]; then
		clear && python3 ./training/run_rspDQN.py
	fi
	if [ "$1" = "ApexDQN" ]; then
		clear && python3 ./training/run_rspApexDQN.py
	fi
	if [ "$1" = "Impala" ]; then
		clear && python3 ./training/run_rspImpala.py
	fi
fi 

