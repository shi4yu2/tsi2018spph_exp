# Usage
## Install all requirements
`$ bash install.sh`

## Launch experiments

* Exp #1: Looking-time infant study
`$ python3 exp1_lookingtime.py [participant_id] [optional - jump to phase 3]`

* Exp #2: 
`$ python3 exp2_axb.py [participant_id]`

## Test

Experiment #1 

* Phase 1
`$ python test_script/test1.py [participant_id]`

* Phase 2
`$ python test_script/test2.py [participant_id]`

* Phase 3
`$ python test_script/test3.py [participant_id]`

Experiment #2
* AXB
`$ python test_script/test_axb.py [participant_id]`

* AV matching
`$ python test_script/test4.py [participant_id]`

## Results

Results files are in `./results/` 

# File dependency

./README.md

## Experiment

```
./2018tsi/
	./README.md
	./install.sh
	./exp1_lookingtime.py
	./exp2_axb.py

	./exp1_p2_stimuli.csv
	./exp1_p3_test_trial.csv

	./results/

	./trial/training.csv
	./libpsypsy/

	./Exp_1_looking_time/
	./Exp_2_axb/
	./Exp_3_av_matching/

	./test_script/
```



