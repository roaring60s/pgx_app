import subprocess
import pandas as pd
pd.set_option("display.max_columns", None)

# header=0 => use first column as the label => "Variant/Haplotypes"
# header=None => add 1 row as label (0-~)

'''
* Run Date -> 27/12/2025
* sample   -> MG2501585
* vcf      -> /media/D1/patients/B000_nara/MG2501585/final/MG2501585.38.raw.dbsnp.FILT.combined.vcf
* Anno:    -> /home/p/mygenics/pipeline_asa_4_FGC_tgx/anno_hs/hs_var_master_grr_14.08.22_EAS_final.txt
'''

# Variables that need to be changed to point to actual directories and files
sf = "/"
maindir = "/media/D1/patients/B000_nara/"
sample = "MG2501585"

# Variables that do not need to be changed if using standard GATK naming convention as per Pawel's Pipeline
vcf = f"{sample}.38.raw.dbsnp.FILT.combined.vcf"
vcf_out = f"{sample}.38.raw.dbsnp.FILT.combined.NHSH.vcf"
sampledir = f"{maindir}{sample}/"
vcf_in = f"{maindir}{sample}/final/{vcf}"
infile1 = f"{maindir}{sample}/{vcf_out}"

# Complex Bash command with pipes, using variable file paths
remove_hash = f"grep '##' -v {vcf_in} > {infile1}"

print(f"starting grep command for sample {sample}")
# Execute the command using subprocess
subprocess.run(remove_hash, shell=True, text=True)

grr = "./annotation/hs_var_master_grr_14.08.22_EAS_final.txt"

outfile1 = f"{sampledir}{sample}_exome_6C.vcf"
outfile2 = f"{sampledir}{sample}_exome_4C.vcf"
S3O1 = f"{sampledir}{sample}.38.MGC.result.S3O1.txt"

out1 = open(outfile1, "w+")
out2 = open(outfile2, "w+")
out3 = open(S3O1, "w+")

print(f"starting pandas to generate input file for MGC/FGC for sample {sample}")

df1 = pd.read_table(infile1, header=0, index_col=False)
df_grr = pd.read_table(grr, header=None, index_col=False)

df1[['GT', 'GTLEFT']] = df1[sample].str.split(':', n=1, expand=True)  # splitting column by delimiter

df1a = df1.drop(['REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', sample, 'GTLEFT'], axis=1)  # removing columns

# print(df1.head(10))

columns = ['#CHROM', 'POS', 'GT', 'ID']  # colums and their order to print

# columns = ['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', sample, 'GTLEFT']  # colums and their order to print
# df1m = pd.merge(df_grr, df1, right_on='ID', left_on=4, how='inner')  # INNER merge
# df1m = df1m.drop(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', sample, 'GTLEFT'], axis=1)

df1mL = pd.merge(df_grr, df1, right_on='ID', left_on=4, how='left')  # LEFT Merge using Column Names

df1mL = df1mL.drop(['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'QUAL', 'FILTER', 'INFO', 'FORMAT', sample, 'GTLEFT'], axis=1)

df1mL = df1mL.fillna('0/0')

# print(df1mL.head(10))

df1mL.to_csv(out3, sep="\t", index=False, header=False)

df1a[columns].to_csv(out2, sep="\t", index=False, header=True)

df1.to_csv(out1, sep="\t", index=False, header=False)

print(f"finished generating MGC/FGC input file from exome for sample {sample}")

print(" ")
print(" ======================================================================== ")
print(f"Starting STEP 2 for sample {sample}")
print(" ")

'''
Generation of PGX input file from exome 6 columns file
'''

# Variables that do not need to be changed if using standard GATK naming convention as per Pawel's Pipeline
snps_var = "./annotation/pgx_asa_variants_snps_master_05.01.2024.txt"

# 'sample'_exome_6C.vcf
infile2 = f"{sampledir}{sample}_exome_6C.vcf"

# Generating asa_7C_hap_'sample'_ST1A.txt
outfile4 = f"{sampledir}pgx_exome_var_{sample}"
out4 = open(outfile4, "w+")

df1 = pd.read_table(infile2, header=None, index_col=False)
df_var = pd.read_table(snps_var, header=None, index_col=False)

dfm = pd.merge(df_var, df1, left_on=2, right_on=2, how='left')

# print(dfm.head(10))
dfm1 = dfm.drop(['0_y', '1_y', '3_y', '4_y', '5_y', '6_y', '7_y', '8_y', '9_y', '11_y'], axis=1)

dfm2 = dfm1.fillna('0/0')
# print(dfm2.head(10))


def categorize_value(value):
    if value == "0/0":
        return "0"
    elif value == "0/1" or "0/2":
        return "1"
    elif value == "1/1" or "1/2" or "2/1" or "2/2":
        return "2"
    else:
        return None  # Handle cases where the value doesn't match any condition


# Create the new column '6' based on the values in column '5'
dfm2['6_y'] = dfm2['10_y'].apply(categorize_value)
#
# print(dfm2.head(10))
#
dfm2.to_csv(out4, sep="\t", index=False, header=False)

# print(dfm2.head(10))

print(" ")
print(" ======================================================================== ")
print(f"Starting STEP 3 for sample {sample}")
print(" ")

'''
Generation of PGX haplotype input file from exome 6 columns
'''

# Variables that do not need to be changed if using standard GATK naming convention as per Pawel's Pipeline
snps_hap = "./annotation/pgx_asa_hap_snps_master_05.01.2024.txt"

# 'sample'_exome_6C.vcf
infile5 = f"{sampledir}{sample}_exome_6C.vcf"

outfile5 = f"{sampledir}pgx_exome_hap_{sample}_ST1A.txt"
out5 = open(outfile5, "w+")

df1 = pd.read_table(infile5, header=None, index_col=False)
df_hap = pd.read_table(snps_hap, header=0, index_col=False)

dfm = pd.merge(df_hap, df1, left_on='hap_var', right_on=2, how='left')

# print(dfm.head(10))

dfm1 = dfm.drop([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11], axis=1)

dfm2 = dfm1.fillna('0/0')

# print(dfm2.head(20))


def categorize_value(value):
    if value == "0/0":
        return "0"
    elif value == "0/1" or "0/2":
        return "1"
    elif value == "1/1" or "1/2" or "2/1" or "2/2":
        return "2"
    else:
        return None  # Handle cases where the value doesn't match any condition


# Create the new column '6' based on the values in column '5'
dfm2[6] = dfm2[10].apply(categorize_value)

dfm2.to_csv(out5, sep="\t", index=False, header=False)


# print(dfm2.head(10))
print(" ")
print(" ======================================================================== ")
print(f"Finished Preprocessing Exome for sample {sample}")
print(" ")
