import sys
import csv

pathx = sys.argv[1]
dir_path = sys.argv[2]

# /media/p/D11/patients/B021_20241213/asa_7C_table3_final_Brand_20834_ST19.txt
prefix1 = "combined_19C_SRT_"
suffix1 = "_ST8.txt"

prefix2 = "table3_final_"
suffix2 = "_ST21.txt"

prefix3 = "table2_input_"
suffix3 = "_ST22.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================


def pgx_table2_input(file1, pref1, suf1, pref2, suf2, pref3, suf3):
	with open(file1, "r") as px:
		counter = 0
		for lnx in px:
			counter = counter + 1
			lsx = lnx.strip().split(s)
			pgx_idx = lsx[2]
			pr1 = pref1
			pr2 = pref2
			pr3 = pref3
			su1 = suf1
			su2 = suf2
			su3 = suf3
			tsv1_path = dir_path + pr1 + pgx_idx + su1
			tsv2_path = dir_path + pr2 + pgx_idx + su2
			tsv3_path = dir_path + pr3 + pgx_idx + su3
			# tsv3_path = open(tsv3_pathin, "w+")
			print(counter, pgx_idx, sep=s)
			
			select_and_save_rows(tsv1_path, tsv2_path, tsv3_path)


def select_and_save_rows(tsv1_path, tsv2_path, tsv3_path):
	
	"""
	Selects rows from TSV1 based on values in TSV2, sorts them,
	and saves specific columns to TSV3.
	
	Args:
		tsv1_path: Path to the first TSV file (TSV1).
		tsv2_path: Path to the second TSV file (TSV2).
		tsv3_path: Path to the output TSV file (TSV3).
	"""

	# 1. Read values from column 5 of TSV2 into a set
	values_to_match = set()
	try:
		with open(tsv2_path, 'r', newline='') as tsv2:
			reader = csv.reader(tsv2, delimiter='\t')
			for row in reader:
				# if len(row) > 4:  # Ensure row has at least 5 columns
				values_to_match.add(row[0])
				# print(row[0])
	except FileNotFoundError:
		print(f"Error: TSV2 file not found at {tsv2_path}")
		return
	except Exception as e:
		print(f"An error occurred while reading TSV2: {e}")
		return
	# print(f"Values to match {s.join(values_to_match)}")

	# 2. Read TSV1, select rows, and store them
	selected_rows = []
	try:
		with open(tsv1_path, 'r', newline='') as tsv1:
			reader = csv.reader(tsv1, delimiter='\t')
			for row in reader:
				# print(f"Found {row[0]}")
				if len(row) > 1 and row[0] in values_to_match:  # Check col2
					selected_rows.append(row)
	except FileNotFoundError:
		print(f"Error: TSV1 file not found at {tsv1_path}")
		return
	except Exception as e:
		print(f"An error occurred while reading TSV1: {e}")
		return
	
	# 3. Sort selected rows based on column 2 (index 1)
	selected_rows.sort(key = lambda row: row[0])

	# 4. Write selected columns to TSV3
	try:
		with open(tsv3_path, 'w', newline='') as tsv3:
			writer = csv.writer(tsv3, delimiter='\t')
			for row in selected_rows:
				if len(row) > 7:  # Ensure row has at least 8 columns
					output_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
						row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]]
					writer.writerow(output_row)
	except Exception as e:
		print(f"An error occurred while writing to TSV3: {e}")
		return


pgx_table2_input(pathx, prefix1, suffix1, prefix2, suffix2, prefix3, suffix3)
