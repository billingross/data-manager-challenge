#!/bin/bash

for filename in input/*.tsv.gz; do
	echo ${filename}
	last_digit=$(echo $(basename ${filename}) | awk -F '.' '{print $1}')
	chromosome=$(echo $(basename ${filename}) | awk -F '.' '{print $2}')
	echo ${last_digit}, ${chromosome}
	
	for ((i=10;i<=14;i++)); do
		start=$(( i * 1000000 ))
    	end=$(( start + 999999 ))
		#gzip -d -c "${filename}" | awk -v start=$start -v end=$end -F '\t' '(($2>=start && $2<=end) || $2=="POS") {print}' > "tasks_output/${last_digit}.chr21_task.${start}_${end}.tsv"
		gzip -d -c "${filename}" | awk -v start=$start -v end=$end -F '\t' '(($2>=start && $2<=end) || $2=="POS") {print}' | gzip > "tasks_output/${last_digit}.${chromosome}.${start}_${end}.tsv.gz"
	done
done