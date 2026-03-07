import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"
#
'''
mgrc_biodata_HS00010001_HS04083572_12C_V1.txt file fields:
A / 0 => mgrc id
F / 5 => patient name
I / 8 => ASA file name
J / 9 => pgx id
K / 10 => exon 9 result
L / 11 => intron 2 result (end of fields)
'''
# =======================================================

prefix1 = "gene_table_input_"
suffix1 = "_ST16.txt"

prefix2 = "table2_final_"
suffix2 = "_ST15.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================

col1 = "DRUG"
col2 = "CATEGORY"
col3 = "GENE"
col4 = "EVIDENCE"
col5 = "EFFECT"
col6 = "GENOTYPE"
col7 = "CLINICAL IMPACT"


# Read the TSV file into a DataFrame
df = pd.read_csv('test_in.txt', delimiter='\t', header=None)

# Assign column names
df.columns = [ 'Gene', 'HAP' ]

# Display the first 5 rows
print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df.info())

# Get all unique values from `Gene`
unique_values = df[ 'Gene' ].unique()

# Check the number of unique values in `Gene`
if len(unique_values) > 50:
	# If there are too many unique values, sample the top 50
	top_occurring_values = df[ 'Gene' ].value_counts().head(50).index.tolist()
	print(top_occurring_values)
else:
	# Otherwise print all unique valus in `Gene`
	print(unique_values)

# Get all unique values from `HAP`
unique_values = df[ 'HAP' ].unique()

# Check the number of unique values in `HAP`
if len(unique_values) > 50:
	# If there are too many unique values, sample the top 50
	top_occurring_values = df[ 'HAP' ].value_counts().head(50).index.tolist()
	print(top_occurring_values)
else:
	# Otherwise print all unique valus in `HAP`
	print(unique_values)

	import numpy as np

# Group by 'Gene' and aggregate 'HAP' values
df_agg = df.groupby('Gene')[ 'HAP' ].agg(lambda x: ' | '.join(x.astype(str))).reset_index()


# Function to sort HAP values
def sort_hap_values(hap_str):
	hap_pairs = hap_str.split(' | ')
	sorted_pairs = [ ]
	for pair in hap_pairs:
		haps = pair.split('/')
		# Extract numeric values
		try:
			val1 = int(haps[ 0 ].split('*')[ 1 ])
			val2 = int(haps[ 1 ].split('*')[ 1 ])
		except ValueError:
			# Handle cases with non-numeric values
			val1 = np.inf
			val2 = np.inf

		# Sort based on numeric values
		sorted_haps = sorted(haps,
		                     key=lambda x: int(x.split('*')[ 1 ]) if x.split('*')[ 1 ].isdigit() else np.inf)
		sorted_pairs.append('/'.join(sorted_haps))
	# Remove duplicates
	sorted_pairs = list(set(sorted_pairs))
	return ' | '.join(sorted_pairs)


# Apply the sorting function to the 'HAP' column
df_agg[ 'HAP' ] = df_agg[ 'HAP' ].apply(sort_hap_values)

# Display the first 5 rows
print(df_agg.head().to_markdown(index=False, numalign="left", stralign="left"))

# Print the column names and their data types
print(df_agg.info())

# Save the DataFrame to a new TSV file
df_agg.to_csv('tsv_out.txt', sep='\t', index=False)
