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

4. Site/time normalization & classification
	- Check the current directory. You need to be at `geo_project/` to run `run_summary.sh`
	```bash
	bash ./run_summary.sh $1 $2 $3 $4 $5 $6 $7
	```
	- e.g., `bash run_summary.sh identification/site_disambiguation.txt classification/data/test_data.txt test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json`
	- input variables: 
		1. result of run_location.sh (e.g., site_disambiguation.txt) ($1)
		2. text file OR directory contains multiple text files (e.g., classification/data/test_data.txt) ($2)
		3. name of following variables:
			* output file name for concatenation (e.g., test_data.txt) ($3)
			* output file name for classification (e.g., test_prediction_result.txt) ($4)
			* output file name for time identification (e.g., test_time_result.json) ($5)
			* output file name for site identification (e.g., test_site_result.json) ($6)
			* output file name for site normalization (e.g., test_norm_result.json) ($7)

	- Running order inside:
		1. concatenation
			* input: text file OR directory contains multiple text files
			* execute: run_summary.sh
			* output: classification/data/$3
		2. classification
			* input: one input file (texts in different lines) 
			* execute file: classification/bin/classification_ensemble_v2.py
			* output: time_recognition/data/$4 ("label'tab'text" in each line)
		3. time identification
			* input: time_recognition/data/$4
			* execute file: time_recognition/bin/find_era.py
			* output: identification/src/main/resources/$5
		4. site identification
			* input: identification/src/main/resources/$5 (time result), $1 (site disambiguation), time_identification/data/$4 (classification result)
			* execute file: identification/src/main/scala/geoscience.scala
			* output: geo_location_norm/src/main/resources/$6
		5. site normalization
			* input: interlim_result.json
			* execute file: geo_location_norm/src/main/scala/Location.scala
			* output: visualization/data/$7
			* 'geonames-index' directory should be located at geo_location_norm (geo_location_norm/geonames-index)
		6. Visualization
			* input: visualization/data/$7
			* execute file: visualization/bin/visualization_top{1|3}.py 
			* output: {Cenozoic|Phanerozoic|Precambrian|Proterozoic}.html
