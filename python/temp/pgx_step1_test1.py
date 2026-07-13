import os
import csv

# /media/p/D11/patients/B020_20241127/asa_7C_020450
# /media/p/D11/patients/B020_20241127/biodata/R20.biodata_master.txt


def process_tsv(biodata_path, tsv_dir, prefix):
	"""
	Processes TSV files based on information from a BIODATA file.

	Args:
		biodata_path (str): Path to the BIODATA.tsv file.
		tsv_dir (str): Directory containing TSV1 and TSV2 files.
		prefix (str): Prefix for the output TSV file name.
	"""

	G1, G2, G3 = "0/0", "0/1", "1/1"  # String variables for GT column
	S1, S2, S3 = 0, 1, 2  # Number variables for SCORE column

	with open(biodata_path, 'r') as biodata_file:
		biodata_reader = csv.reader(biodata_file, delimiter='\t')
		# next(biodata_reader)  # Skip header if present
		for row in biodata_reader:
			pattern = prefix + row[2]  # String pattern from column 4 of BIODATA

			# Find TSV1 file based on the pattern
			tsv1_file = None
			for filename in os.listdir(tsv_dir):
				# if pattern in filename and filename.endswith(".tsv"):
				if pattern in filename:
					tsv1_file = os.path.join(tsv_dir, filename)
					break

			if tsv1_file:
				# dir_path + "hap_" + pgx_idx + "_ST1A.txt"
				tsv2_file = os.path.join(tsv_dir, pattern + "_ST1B.txt")  # Construct TSV2 file name

				# Process TSV1 and TSV2
				process_tsv_pair(tsv1_file, tsv2_file, G1, G2, G3, S1, S2, S3, prefix)


def process_tsv_pair(tsv1_file, tsv2_file, G1, G2, G3, S1, S2, S3, prefix):
	"""
	Processes a pair of TSV1 and TSV2 files.

	Args:
		tsv1_file (str): Path to the TSV1 file.
		tsv2_file (str): Path to the TSV2 file.
		G1, G2, G3 (str): String variables for GT column.
		S1, S2, S3 (int): Number variables for SCORE column.
		prefix (str): Prefix for the output TSV file name.
	"""

	output_data = []
	seen_rows = set()

	with open(tsv1_file, 'r') as tsv1, open(tsv2_file, 'r') as tsv2:
		tsv1_reader = csv.reader(tsv1, delimiter='\t')
		tsv2_reader = csv.reader(tsv2, delimiter='\t')
		next(tsv1_reader)  # Skip header if present
		next(tsv2_reader)  # Skip header if present

		for row1 in tsv1_reader:
			tsv2.seek(0)  # Reset TSV2 file pointer to the beginning for each row1
			for row2 in tsv2_reader:
				if row1[9] == row2[0]:  # if TSV1 col1 == TSV2 col2
					if row2[3] == row2[4] and row2[3] == row1[3]:
						output_row = row1 + [G1, S1]
					elif row2[3] == row2[4] and row2[3] == row1[1]:
						output_row = row1 + [G2, S2]
					elif row2[3] != row2[4]:
						output_row = row1 + [G3, S3]
					else:
						continue  # Skip if no conditions are met

					# Remove duplicates
					row_tuple = tuple(output_row)
					if row_tuple not in seen_rows:
						seen_rows.add(row_tuple)
						output_data.append(output_row)

	# Save to new TSV file
	output_filename = f"{prefix}_{os.path.basename(tsv1_file)}"
	with open(output_filename, 'w', newline='') as outfile:
		tsv_writer = csv.writer(outfile, delimiter='\t')
		tsv_writer.writerows(output_data)