#!/usr/bin/env bash
file="GPL16304-47833.txt.gz"
if [ -e $file ] 
then
	python3 CreateDNAmethDataCommands.py
	bash DNA_MethylationFiles.sh
	rm DNA_MethylationFiles.sh
else
	wget "https://www.dropbox.com/s/8m7ourb5ucyvcf6/GPL16304-47833.txt.gz?dl=0&file_subpath=%2FGPL16304-47833.txt"
	mv 'GPL16304-47833.txt.gz?dl=0&file_subpath=%2FGPL16304-47833.txt' $file
#	 for c in `cat CancerTypes.txt`; do
#	    echo "somefile_${c}.txt"; done;
	python3 CreateDNAmethDataCommands.py
    bash DNA_MethylationFiles.sh
    rm DNA_MethylationFiles.sh
fi
rm $file

cd output_Data
mv *.* ../../
cd ../
rmdir output_Data
cd ../
if [ -d "InputData" ]
then
    mv TCGA*.tsv InputData/
else
    mkdir InputData
    mv TCGA*.tsv InputData/
fi
cd InputData
for file in `ls `; do
    IFS='.' read -ra cancertype <<< "$file"
    mydir="${cancertype[0]}"
    if [ -d $mydir"/DNA_Methylation/" ]
    then
        mv $mydir".tsv" $mydir/DNA_Methylation/
    else
        if [ -d $mydir ]
        then
            mkdir $mydir/DNA_Methylation
            mv $mydir".tsv" $mydir/DNA_Methylation/
        else
            mkdir $mydir
            mkdir $mydir/DNA_Methylation
            mv $mydir".tsv" $mydir/DNA_Methylation/
        fi
    fi
done
