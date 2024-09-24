#!/usr/bin/env python3

import os
import pdb
import glob
import gzip

import pandas as pd

from functools import reduce

info_columns = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']

input_directory = "exercise_input_data_public"

tsv_files =  glob.glob(f"{input_directory}/*.tsv.gz")
print(f"Found {len(tsv_files)} input files.")

tsv_subset = tsv_files[0:5]

tsv_frames = [pd.read_csv(tsv, compression='gzip', header=0, sep='\t') for tsv in tsv_subset]
pdb.set_trace()
#concat_frame = pd.concat(tsv_frames, axis=1)
#pdb.set_trace()
#joined_frame = tsv_frames[0].join(tsv_frames[1], on=variant_info_columns)
#pdb.set_trace()
merged_frame = pd.merge(
						left=tsv_frames[0],
						right=tsv_frames[1],
						how='left',
						left_on=info_columns,
						right_on=info_columns)
pdb.set_trace()

reduce_merged_frame = reduce(lambda  left,right: pd.merge(left,right,on=info_columns,how='outer'), tsv_frames)
pdb.set_trace()

#for file in tsv_files:
#	df = pd.read_csv(file, compression='gzip', header=0, sep='\t')
#	pdb.set_trace()

"""Read file to see what it looks like
for file in tsv_files:
	with gzip.open(file, 'r') as file_handle:
		for line in file_handle:
			print(line)
			pdb.set_trace()

Ouput:
b'#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tHG00145\n'
b'21\t10000025\trs530469795\tTA\tT\t100\tPASS\tAC=41;AF=0.0081869;AN=5008;NS=2504;DP=17454;EAS_AF=0.005;AMR_AF=0;AFR_AF=0.0265;EUR_AF=0;SAS_AF=0.001;AA=|||unknown(NO_COVERAGE);VT=INDEL\tGT\t0|0\n'
"""