#!/bin/bash

# $0 = run_summary.sh
# $1 = site disambigutation file (e.g., site_disambiguation.txt)
# $2 = input file / dir
# e.g., (dir) ./src/main/resources/json
# e.g., (file) sample.txt 
# $3 = output of concatenation (e.g., text_input.txt)
# $4 = output of classification (e.g., prediction_result.txt)
# $5 = output of time identification (e.g., time_resut.json)
# $6 = output of site identification (e.g., site_result.json)
# $7 = output of site normalization (e.g., norm_result.json)
# e.g., 
# bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt texitest_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json

current_dir=$PWD
classification_dir=$PWD/classification
time_identification=$PWD/time_recognition
site_identification=$PWD/identification
site_normalization=$PWD/geo_location_norm
visualization_dir=$PWD/visualization

echo "========================"
echo "classification: $classification_dir"
echo "time_identification: $time_identification"
echo "site_identification: $site_identification"
echo "site_normalization: $site_normalization"
echo "visualization: $visualization_dir"
echo "========================"


echo "========================"
echo "0. Check file"
echo "========================"


mkdir -p $current_dir/temp

for file in $current_dir/$2/*.json; do
	# echo "$file"
	if grep -q volcanism "$file"; then
		if grep -q climate "$file"; then
			cp $file $current_dir/temp/
		fi
	elif grep -q magmatism "$file"; then
		if grep -q climate "$file"; then
			cp $file $current_dir/temp/
		fi
	fi
done 

echo "There are"
ls $current_dir/temp | wc -l 
echo "files containing (volcanism|magmatism) and climate"

echo "========================"
echo "1. Classification"
echo "========================"

cd $classification_dir/bin
echo $PWD

python3 ./classification_ensemble_v2.py $current_dir/temp $time_identification/data/$4

echo "========================"
echo "2. Time identification"
echo "========================"

cd $time_identification/bin
echo $PWD

python3 ./find_era.py ../data/$4 $site_identification/src/main/resources/$5

echo "========================"
echo "3. Site identification"
echo "========================"

cd $site_identification
echo $PWD

export SBT_OPTS="-XX:+CMSClassUnloadingEnabled -XX:MaxPermSize=16G -Xmx16G"

sbt "runMain geoscience.GeoscienceExample $site_identification/src/main/resources/$5 $current_dir/$1 $time_identification/data/$4 $site_normalization/src/main/resources/$6"


echo "========================"
echo "4. Site normalization"
echo "========================"

cd $site_normalization
echo $PWD

sbt "runMain location_norm.GeoLocationExample $site_normalization/src/main/resources/$6 $visualization_dir/data/$7"

echo "========================"
echo "5. Visualizaion"
echo "========================"

cd $visualization_dir/bin

if [ ! -d ../maps ]; then
	mkdir ../maps
fi
if [ ! -d ../maps/top1 ]; then
	mkdir ../maps/top1
fi
if [ ! -d ../maps/top3 ]; then
	mkdir ../maps/top3
fi


python3 ./visualization_top1.py ../data/$7 
python3 ./visualization_top3.py ../data/$7 

echo "========================"
echo "DONE"
echo "========================"

rm -rf $current_dir/temp