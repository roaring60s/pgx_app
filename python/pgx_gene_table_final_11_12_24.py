import sys
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"
# /media/p/D11/patients/B017_20241003/asa_7C_gene_table_input_20625_ST16.txt


# =======================================================

prefix1 = "gene_table_input_"
suffix1 = "_ST16.txt"

prefix2 = "gene_table_final_"
suffix2 = "_ST17.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================


def pgx_gene_final_table(file1, pref1, suf1, pref2, suf2):
	with open(file1, "r") as px:
		counter = 0
		for lnx in px:
			counter = counter + 1
			lsx = lnx.strip().split(s)
			pgx_idx = lsx[2]
			pr1 = pref1
			pr2 = pref2
			su1 = suf1
			su2 = suf2
			path_in = dir_path + pr1 + pgx_idx + su1
			path_out = dir_path + pr2 + pgx_idx + su2
			fileout = open(path_out, "w+")
			print(counter, pgx_idx, sep=s)

			# Read the TSV file into a DataFrame
			df = pd.read_csv(path_in, delimiter='\t', header=None)

			# Assign column names
			df.columns = ['Gene', 'HAP']

			# Display the first 5 rows
			print(df.head().to_markdown(index=False, numalign="left", stralign="left"))

			# Print the column names and their data types
			# print(df.info())

			# Get all unique values from `Gene`
			unique_values = df['Gene'].unique()

			# Check the number of unique values in `Gene`
			if len(unique_values) > 50:
				# If there are too many unique values, sample the top 50
				# top_occurring_values = df['Gene'].value_counts().head(50).index.tolist()
				print(top_occurring_values)
			else:
				# Otherwise print all unique valus in `Gene`
				print(unique_values)

			# Get all unique values from `HAP`
			unique_values = df['HAP'].unique()

			# Check the number of unique values in `HAP`
			if len(unique_values) > 50:
				# If there are too many unique values, sample the top 50
				top_occurring_values = df['HAP'].value_counts().head(50).index.tolist()
				print(top_occurring_values)
			else:
				# Otherwise print all unique valus in `HAP`
				print(unique_values)

			# Group by 'Gene' and aggregate 'HAP' values
			df_agg = df.groupby('Gene')['HAP'].agg(lambda x: ' | '.join(x.astype(str))).reset_index()

			# Apply the sorting function to the 'HAP' column
			df_agg['HAP'] = df_agg[ 'HAP' ].apply(sort_hap_values)

			# Display the first 5 rows
			print(df_agg.head().to_markdown(index=False, numalign="left", stralign="left"))

			# Print the column names and their data types
			# print(df_agg.info())

			# Save the DataFrame to a new TSV file
			df_agg.to_csv(fileout, sep='\t', index=False)


# Function to sort HAP values
def sort_hap_values(hap_str):
	hap_pairs = hap_str.split(' | ')
	sorted_pairs = [ ]
	for pair in hap_pairs:
		haps = pair.split('/')
		# Extract numeric values
		try:
			val1 = int(haps[0].split('*')[1])
			val2 = int(haps[1].split('*')[1])
		except ValueError:
			# Handle cases with non-numeric values
			val1 = np.inf
			val2 = np.inf

		# Sort based on numeric values
		sorted_haps = sorted(haps, key=lambda x: int(x.split('*')[1]) if x.split('*')[1].isdigit() else np.inf)
		sorted_pairs.append('/'.join(sorted_haps))
	# Remove duplicates
	sorted_pairs = sorted(set(sorted_pairs))
	return ' | '.join(sorted_pairs)


pgx_gene_final_table(pathx, prefix1, suffix1, prefix2, suffix2)
