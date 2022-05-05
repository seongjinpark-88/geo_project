# How to Run the code

1. Build docker container by running `sudo bash ./build_container.sh`

2. Start docker container by running `sudo bash ./start_container.sh`

3. Co-occurrence: need to be executed separately (to disambiguate unrecognizeable sites)
	```bash
	cd identification
	bash ./run_location.sh {input} {output}
	```
	- e.g., `bash ./run_location.sh  ./src/main/resources/json site_disambiguation.txt`
	- input: text file OR directory contains multiple text files
	- output: tab separated text file
	- the result file is already included in the repo.

4. Site/time normalization & classification
	- Check the current directory. You need to be at `geo_project/` to run `run_summary.sh`
	- e.g., `bash run_summary.sh identification/site_disambiguation.txt classification/data/processed_data.txt train_data.txt train_prediction_result.txt train_time_result.json train_site_result.json train_norm_result.json`
	- input variables: 
		1. result of run_location.sh (e.g., site_disambiguation.txt) ($1)
		2. directory contains multiple json files (e.g., classification/sample_jsons) or one text file that each document is in one line ($2)
		3. the names of output files are defined in run_summary.sh:
			* output file of classification: train_prediction_result.txt
			* output file of time identification: train_time_result.json
			* output file of site identification: train_site_result.json
			* output file of site normalization: train_norm_result.json

	- Running order inside:
		1. classification
			* input: one input file (texts in different lines) 
			* execute file: classification/bin/classification_ensemble_v2.py
			* output: time_recognition/data/train_prediction_result.txt ("label'tab'text" in each line)
		2. time identification
			* input: time_recognition/data/train_prediction_result.txt
			* execute file: time_recognition/bin/find_era.py
			* output: identification/src/main/resources/train_time_result.json
		3. site identification
			* input: identification/src/main/resources/train_time_result.json, $1 (site disambiguation), time_identification/data/train_prediction_result.txt
			* execute file: identification/src/main/scala/geoscience.scala
			* output: geo_location_norm/src/main/resources/train_site_result.json
		4. site normalization
			* input: geo_location_norm/src/main/resources/train_site_result.json
			* execute file: geo_location_norm/src/main/scala/Location.scala
			* output: visualization/data/train_norm_result.json
			* 'geonames-index' directory should be located at geo_location_norm (geo_location_norm/geonames-index)
		5. Visualization
			* input: visualization/data/train_norm_result.json
			* execute file: visualization/bin/visualization_top{1|3}.py 
			* output: visualization/maps/top{1|3}/{Cenozoic|Phanerozoic|Precambrian|Proterozoic}.html
