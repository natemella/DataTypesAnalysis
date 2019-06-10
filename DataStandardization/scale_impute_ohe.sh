#!/usr/bin/env bash
set -e
scaling() {
path=$1
filename=$2
docker run --rm -i \
  -v $path:"/InputData" \
  --user $(id -u):$(id -g) \
  srp33/shinylearner:version513 \
    python3 /scripts/Scale.py /InputData/${filename} true robust

}

imputing() {
path=$1
filename=$2
echo $path
docker run --rm -i \
  -v $path:"/InputData" \
  --user $(id -u):$(id -g) \
  srp33/shinylearner:version513 \
    Rscript --vanilla /scripts/Impute.R /InputData/${filename} true

}

one-hot_encoding() {
path=$1
filename=$2
docker run --rm -i \
  -v $path:"/InputData" \
  --user $(id -u):$(id -g) \
  srp33/shinylearner:version513 \
    python3 /scripts/OneHotEncode.py /InputData/${filename}

}

get_extension() {
filename=$1
IFS='.' read -ra mylist <<< "$filename"
extension="${mylist[1]}"
echo $extension
}

gzip_all_files() {
datatype=$1
    echo our data type is $datatype
    for file in `ls $datatype`; do
        if [[ $datatype == "Covariate" ]] && [[ $extension == "tsv" ]]; then
            continue
        fi
        gzip $datatype/$file
    done
}
cd ..
echo step one
pwd
search_dir=InputData
for CancerType in `ls $search_dir`; do
	cd $search_dir
	echo step two
	pwd
	for datatype in `ls $CancerType`; do
	    if [[ $datatype == "Class" ]]; then
	        continue
	    fi
		cd $CancerType
		echo step three
		pwd
	    gzip_all_files `pwd`/$datatype
		if [[ $datatype =~ ^(Covariate|Expression|RPPA|miRNA)$ ]]; then
			for file in `ls $datatype`; do
			    extension=$(get_extension ${file})
			    if [[ $datatype == "Covariate" ]] && [[ $extension == "tsv" ]]; then
			        continue
			    fi
				echo SCALING $file
				scaling ${datatype} $file
				echo ------------------
			done
		fi
		for file in `ls $datatype`; do
		    if [[ $datatype == "Covariate" ]] && [[ $extension == "tsv" ]]; then
			        continue
			fi
		    echo IMPUTING $file
		    imputing ${datatype} $file
		    echo ------------------
		    echo One-hot encoding $file
		    one-hot_encoding ${datatype} $file
		    gunzip $datatype/$file
		done
	    cd ../
	done
	cd ../
done