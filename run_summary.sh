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
# bash run_summary.sh identification/site_disambiguation.txt classification/sample_json 
# test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json

# bash run_summary.sh identification/site_identification.txt classification/sample_json

current_dir=$PWD
classification_dir=$PWD/classification
time_identification=$PWD/time_recognition
site_identification=$PWD/identification
site_normalization=$PWD/geo_location_norm
visualization_dir=$PWD/visualization


classification_output=test_prediction_result.txt
time_output=test_time_result.json
site_output=test_site_result.json
norm_output=test_norm_result.json

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
mkdir -p $current_dir/outputs

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

python3 ./classification_ensemble_v2.py $current_dir/temp $time_identification/data/$classification_output
cp $time_identification/data/$classification_output $current_dir/outputs/

echo "========================"
echo "2. Time identification"
echo "========================"

cd $time_identification/bin
echo $PWD

python3 ./find_era.py ../data/$classification_output $site_identification/src/main/resources/$time_output
cp $site_identification/src/main/resources/$time_output $current_dir/outputs/

echo "========================"
echo "3. Site identification"
echo "========================"

cd $site_identification
echo $PWD

export SBT_OPTS="-XX:+CMSClassUnloadingEnabled -XX:MaxPermSize=16G -Xmx16G"

sbt "runMain geoscience.GeoscienceExample $site_identification/src/main/resources/$time_output $current_dir/$1 $time_identification/data/$classification_output $site_normalization/src/main/resources/$site_output"

cp $site_normalization/src/main/resources/$site_output $current_dir/outputs/

echo "========================"
echo "4. Site normalization"
echo "========================"

cd $site_normalization
echo $PWD

sbt "runMain location_norm.GeoLocationExample $site_normalization/src/main/resources/$site_output $visualization_dir/data/$norm_output"
cp $visualization_dir/data/$norm_output $current_dir/outputs/

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


python3 ./visualization_top1.py ../data/$norm_output 
python3 ./visualization_top3.py ../data/$norm_output

cp -r $visualization_dir/maps $current_dir/outputs/

echo "========================"
echo "DONE"
echo "========================"

rm -rf $current_dir/temp