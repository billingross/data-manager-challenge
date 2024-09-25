#!/usr/bin/env python3

import os
import pdb
import glob
import gzip

import pandas as pd

from pathlib import Path
from functools import reduce

def get_allele_count(genotype, allele):
	#pdb.set_trace()
	alleles = genotype.split('|')
	return alleles.count(str(allele))

info_columns = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']
input_directory = "exercise_input_data_public"

tsv_files =  glob.glob(f"{input_directory}/*.tsv.gz")
print(f"Found {len(tsv_files)} input files.")

### Read, parse, and clean input data
# Read every TSV file into a dataframe
tsv_frames = [pd.read_csv(tsv, compression='gzip', header=0, sep='\t') for tsv in tsv_files]

# Merge all dataframes on the variant info columns
reduce_merged_df = reduce(lambda  left,right: pd.merge(left,right,on=info_columns,how='outer'), tsv_frames)

# Rename sample
cleaned_df = reduce_merged_df.rename(columns={'HG10101':'HG00101'})
###

### Count alleles
# Create a dataframe that only includes sample genotype values
genotypes_df = cleaned_df.filter(regex='HG')

# Convert genotypes to major and minor allele counts per each site and sample
major_ac_df = genotypes_df.map(get_allele_count, allele='0')
minor_ac_df = genotypes_df.map(get_allele_count, allele='1')

# Sum major and minor allele counts across sites (per sample)
sum_major_ac_df = major_ac_df.apply(sum, axis=0)
sum_minor_ac_df = minor_ac_df.apply(sum, axis=0)

# Combine major and minor allele counts into single dataframe
allele_count_df = pd.concat([sum_major_ac_df, sum_minor_ac_df], axis=1)
allele_count_df.columns = ['major_count', 'minor_count']

# Write allele counts dataframe to TSV
allele_count_df.to_csv("allele_counts.tsv", sep='\t', index_label="sample_id")
###


### Subset and save new files
# Create output directory
Path("output").mkdir(parents=False, exist_ok=True)

# Subset data and write to new files
variant_info_df = cleaned_df.iloc[:, :9]
for i in range(0,10):
	sample_subset_df = cleaned_df.filter(regex=f"{i}$")
	subset_df = pd.concat([variant_info_df, sample_subset_df], axis=1)
	print(f"Subset dataframe shape: {subset_df.shape}.")
	subset_df.to_csv(
					 f"output/{i}.chr21.10000000_14999999.tsv.gz",
					 sep='\t',
					 index=False)
###