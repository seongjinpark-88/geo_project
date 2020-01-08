#!/bin/bash

# $0 = run_location.sh
# $1 = input file / dir
# e.g., (dir) ./src/main/resources/json
# e.g., (file) sample.txt 
# $2 = output file
# e.g., output.txt

export SBT_OPTS="-XX:+CMSClassUnloadingEnabled -XX:MaxPermSize=8G -Xmx8G"

if [[ -d $1 ]]; then
	echo "Your input is a directory"
	# Open JSON files and Create temporary file
	for file in $1/*; do
		cat $file >> tmp_text.txt
	done

	currentDIR=$PWD

	sbt "runMain cooccurrence.CooccurrenceExample $PWD/tmp_text.txt $2"

	rm tmp_text.txt
elif [[ -f $1 ]]; then
	echo "Your input is a file"

	currentDIR=$PWD

	sbt "runMain cooccurrence.CooccurrenceExample $PWD/$1 $2"
fi
