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
    python3 /scripts/Scale.py /InputData/${filename} true robust

}

get_extension() {
filename=$1
IFS='.' read -ra mylist <<< "$filename"
extension="${mylist[1]}"
echo $extension
}

cd ..
search_dir=InputData
for CancerType in `ls $search_dir`; do
	cd $search_dir
	for datatype in `ls $CancerType`; do
	    if [[ $datatype == "Class" ]]; then
	        continue
	    fi
		cd $CancerType
		if [[ $datatype =~ ^(Covariate|Expression|RPPA|miRNA)$ ]]; then
			for file in `ls $datatype`; do
			    extension=$(get_extension ${file})
			    if [[ $datatype == "Covariate" ]] && [[ $extension == "tsv" ]]; then
			        continue
			    fi
				echo `pwd`
				gzip $datatype/$file
				echo SCALING $file
				scaling `pwd` $file
				echo ------------------
			done
		fi
		for file in `ls $datatype`; do
		    echo `pwd`
		    gzip $datatype/$file
		    echo IMPUTING $file
		    imputing `pwd` $file
		    echo ------------------
		    echo One-hot encoding $file
		    one-hot_encoding `pwd` $file
		    gunzip $datatype/$file
		done
	    cd ../
	done
	cd ../
done