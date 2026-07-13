

def reformat_tsv(file1, dir_path, pref1, suf1, pref2, suf2):
	"""
	Reformats a TSV file by vertically listing comma-separated values in specified columns.
	
	Args:
	input_file: Path to the input TSV file.
	output_file: Path to the output TSV file.
	"""
	s = '\t'
	
	with open(file1, "r") as px:
		counter = 0
		for lnx in px:
			counter = counter + 1
			lsx = lnx.strip().split('\t')
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
						# Reformat columns
						for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]:
							if i < len(parts):
								if ',' in parts[i]:
									parts[i] = parts[i].replace('"', '')
									parts[i] = '"' + '\n'.join(parts[i].split(',')) + '"'
									columns.append(parts[i])
								else:
									columns.append(parts[i])
						
						outfile.write('\t'.join(columns) + '\n')
			
			except FileNotFoundError:
				print(f"Error: Input file '{path_in}' not found.")
			except Exception as e:
				print(f"An error occurred: {e}")
