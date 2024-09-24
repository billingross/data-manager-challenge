#!/usr/bin/env python3

import os
import pdb
import glob
import gzip

import pandas as pd

from functools import reduce

def get_allele_count(genotype, allele):
	#pdb.set_trace()
	alleles = genotype.split('|')
	return alleles.count(str(allele))

info_columns = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']

input_directory = "exercise_input_data_public"

tsv_files =  glob.glob(f"{input_directory}/*.tsv.gz")
print(f"Found {len(tsv_files)} input files.")

tsv_frames = [pd.read_csv(tsv, compression='gzip', header=0, sep='\t') for tsv in tsv_files]

merged_df = pd.merge(
					 left=tsv_frames[0],
					 right=tsv_frames[1],
					 how='left',
					 left_on=info_columns,
					 right_on=info_columns)

reduce_merged_df = reduce(lambda  left,right: pd.merge(left,right,on=info_columns,how='outer'), tsv_frames)
#pdb.set_trace()

cleaned_df = reduce_merged_df.rename(columns={'HG10101':'HG00101'})
#pdb.set_trace()

# Create a dataframe that only includes sample genotype values
genotypes_df = cleaned_df.filter(regex='HG')

# Convert genotypes to major and minor allele counts per each site and sample
major_ac_df = genotypes_df.applymap(get_allele_count, allele='0')
minor_ac_df = genotypes_df.applymap(get_allele_count, allele='1')

# Sum major and minor allele counts across sites (per sample)
sum_major_ac_df = major_ac_df.apply(sum, axis=0)
sum_minor_ac_df = minor_ac_df.apply(sum, axis=0)

# Combine major and minor allele counts into single dataframe
allele_count_df = pd.concat([sum_major_ac_frame, sum_minor_ac_frame], axis=1)
allele_count_df.columns = ['major_count', 'minor_count']
pdb.set_trace()

# Write allele counts dataframe to TSV
allele_count_df.to_csv("allele_counts.tsv", sep='\t', index_label="sample_id")

#major_af_frame = genotypes_frame.apply(get_allele_count, args=1, axis=1)
#pdb.set_trace()

# Create a new table with major and minor allele counts
# 0 = major
# 1 = minor
# "0|0" = 2 major, 0 minor

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