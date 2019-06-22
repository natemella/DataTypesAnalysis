#!/usr/bin/env bash
file_to_delete=Clinical
cd ..
search_dir=InputData
for CancerType in `ls $search_dir`; do
	echo our cancer type is $CancerType
	cd $search_dir
	for datatype in `ls $CancerType`; do
		cd $CancerType
		if [ "$datatype" = "$file_to_delete" ]
		then
			echo our datatype is $datatype
			for file in `ls $datatype`; do
				echo our file to delete is $file
				cd $datatype
				rm $file
				cd ../
			done
		fi
	    cd ../
	done
	cd ../
done
#IFS='.' read -ra Analysis <<< "$file"
#echo "${Analysis[0]}"
