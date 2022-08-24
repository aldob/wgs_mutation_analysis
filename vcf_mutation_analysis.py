import os 
import pandas as pd

# Create a list of VCF files that are to be filtered
os.chdir("path/to/vcf/files")
files = [fil for fil in os.listdir("./") if fil.endswith(".vcf")]

out_dict = {fil:[] for fil in files}
# Loop through each of the VCF files
for fil in files:
    print(fil)

    # 
    with open(fil) as vcf:

        # Loop through each line in the VCF
        for line in vcf:
            # '#' marks the header lines so ignore those
            if not line.startswith("#"):
                columns = line.split("\t")
                # Add the columns of each VCF to the dictionary entry for that file
                out_dict[fil]+=[columns]



# Create a dataframe where the columns are the VCF file names and the indices are the mtuation types 
mut_df = pd.DataFrame(1, columns=list(files), index=["Substitutions", "Small Deletions", "Large Deletions"])
#### Large del #####
for k, v in out_dict.items():
    for columns in v:
        if "," not in columns[5]:
            # If large deletion
            if 5 <= len(columns[4]) - len(columns[5]):
                mut_df.at["Large Deletions", k]+=1
            # If substitution
            if len(columns[4]) - len(columns[5]) == 0:
                for b,s in zip(columns[4], columns[5]):
                    if b != s:
                        mut_df.at["Substitutions", k]+=1
            # If small deletion
            if 0 < len(columns[4]) - len(columns[5]) < 5:
                mut_df.at["Small Deletions", k]+=1   
        # If there is a ',' then multiple mutant alleles have been called and need to be handled seperately                      
        else:
            # Loop through each allele
            for allele in columns[5].split(","):
                # If large deletion
                if 5 <=  len(columns[4]) - len(allele):
                    mut_df.at["Large Deletions", k]+=1
                # If substitution
                elif len(columns[4]) - len(allele) == 0:
                    for b,s in zip(columns[4], allele):
                        if b != s:
                            mut_df.at["Substitutions", k]+=1                    
                # If small deletion
                elif 0 < len(columns[4]) - len(allele) < 5:
                    mut_df.at["Small Deletions", k]+=1

mut_df.to_csv("mutation_table.csv", index=True, header=True)


