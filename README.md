# Mutation Analysis Scripts
Custom scripts used for the filtering and analysis of VCF files from whole genome sequencing datasets.
<br>
<br>

## vcf_quality_filtering.py

Takes VCF files and generates new, filtered VCF files where all mutaiton calls have been filtered so that they must be above certain quality levels. Quality filtered by default is TOLD > 6.3 and NLOD > 2.2

## vcf_mutation_analysis.py

Parses through batches of VCF files to calculate the total level of different mutation types in each file. The final output is written as a .csv containing the results for all files.
