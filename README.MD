Run:
	1. Co-occurrence: need to be executed separately (to disambiguate unrecognizeable sites)
		- run_location.sh
		- input: text file OR directory contains multiple text files
		- output: variable

	2. Site/time normalization & classification
		- run_summary.sh
		- input variables: 
			1. result of run_location.sh (one text file) ($1)
			2. text file OR directory contains multiple text files ($2)
			3. name of following variables:
				* output of concatenation ($3)
				* output of classification ($4)
				* output of time identification ($5)
				* output of site identification ($6)
				* output of site normalization ($7)

		- running order:
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

			6. Visualization
				* input: visualization/data/$7
				* execute file: visualization/bin/visualization_top{1|3}.py 
				* output: {Cenozoic|Phanerozoic|Precambrian|Proterozoic}.html