import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

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

# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_table3_final_19719_ST18.txt

prefix1 = "table3_Brand_"
suffix1 = "_ST20.txt"

prefix2 = "table3_final_"
suffix2 = "_ST21.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================


def reformat_tsv(file1, pref1, suf1, pref2, suf2):
	"""
	Reformats a TSV file by vertically listing comma-separated values in specified columns.
	
	Args:
	input_file: Path to the input TSV file.
	output_file: Path to the output TSV file.
	"""
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
			print(counter, pgx_idx, sep=s)
	
			try:
				with open(path_in, 'r', encoding='utf-8') as infile, open(path_out, 'w', encoding='utf-8') as outfile:
					for line in infile:
						parts = line.strip().split('\t')
						
						columns = []
						# Reformat columns 1, 3 and 6
						for i in [0, 1, 2, 3, 4, 5]:
							if i < len(parts):
								if ',' in parts[i]:
									parts[i] = parts[i].replace('"','')
									parts[i] = '"' + '\n'.join(parts[i].split(',')) + '"'
									columns.append(parts[i])
								else:
									columns.append(parts[i])
						
						outfile.write('\t'.join(columns) + '\n')
			
			except FileNotFoundError:
				print(f"Error: Input file '{path_in}' not found.")
			except Exception as e:
				print(f"An error occurred: {e}")


reformat_tsv(pathx, prefix1, suffix1, prefix2, suffix2)
