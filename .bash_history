ls
cd classification
ls
cd ..
ls
cd identification/
ls
bash run_location.sh ../classification/sample_jsons site_disambiguation.txt
ls
cat site_disambiguation.txt | wc -l
cd ..
ls
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
ls
cd identification/
ls
cd src/main/resources/
ls
head sample_time_result.json 
cd ..
ls
cd ..
ls
cd ..
ls
cd ..
ls
cd time_recognition/
ls
cd data
ls
head sample_prediction_result.txt 
cd ..
ls
cd ..
ls
cd classification/
ls
cd bin
ls
python classification_ensemble_v2.py ../sample_jsons/ tmp.txt
pip install sklearn
python classification_ensemble_v2.py ../sample_jsons/ tmp.txt
pip install scikit-learn
pip3 install scikit-learn
python
python3 classification_ensemble_v2.py ../sample_jsons/ tmp.txt
ls
head tmp.txt 
cd ..
ls
cd ..
ls
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
ls
vim run_summary.sh 
vi run_summary.sh 
exit
exit
ls
cat run_summary.sh 
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
bash ./run_summary.sh identification/site_disambiguation.txt classification/sample_jsons sample_data.txt sample_prediction_result.txt sample_time_result.json sample_site_result.json sample_norm_result.json
exit
exit
ls
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
ls
cd data
ls
cd ..
cd time_recognition/
ls
cd data
ls
head test_prediction_result.txt 
ls
cd ..
ls
cd ..
ls
cd classification/
ls
cd sample_jsons/
ls
cat * | grep "volcanism" | grep "climate"
cat * | grep "volcanism" | grep "climate" | wc -l
cat * | grep "magmatism" | grep "climate" | wc -l
cd ..
ls
cd ..
ls
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
cd classification/sample_jsons/
ls
cat * | grep "volcanism" | wc -l
cd ..
cd ..
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
pwd
ls classification/sample_jsons/ | wc -l
ls classification/sample_jsons/*.json | wc -l
for file in classification/sample_jsons/*.json; do if grep -q volcanism "$file"; then echo "1"; done
for file in classification/sample_jsons/*.json; do if grep -q volcanism "$file"; then echo "1"; fi; done
ls
cd temp
ls
cd ..
ls
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
cwd
pwd
for file in classification/sample_jsons/*.json; do if grep -q volcanism "$file"; then if grep -q climate "$file"; then echo "1"; fi; fi; done
bash run_summary.sh identification/site_disambiguation.txt classification/sample_json test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
ls
cd classification/
ls
cd ..
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
sbt
sbt cancel
cd identification/
sbt
jstack
jstack -l
pgrep sbt
cd ..
pgrep ivy
ps/htop
ps
exit
exit
ps
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
exit
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
head time_recognition/data/test_prediction_result.txt 
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
bash run_summary.sh identification/site_disambiguation.txt classification/sample_jsons test_data.txt test_prediction_result.txt test_time_result.json test_site_result.json test_norm_result.json
exit
exit
