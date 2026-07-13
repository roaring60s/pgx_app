# from decorator import append


def capitalise_word(file1, dir_path, pref1, suf1, pref2, suf2):
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
						columns = line.strip().split('\t')
						col_number = len(columns)
						parts = []
						
						# Reformat columns
						list_index = range(col_number)
						for i in list_index:
							if i < 2:
								parts.append(columns[i])
							if 2 <= i < col_number:
								if columns[i] == "":
									columns_cap.append("NA")
								else:
									print(columns[i])
									columns[i] = columns[i].replace('"', '')
									print(columns[i])
									columns_cap = [word.capitalize() for word in columns[i].split(',')]
									parts.append(columns_cap)
								
						outfile.write('\t'.join(parts) + '\n')
			
			except FileNotFoundError:
				print(f"Error: Input file '{path_in}' not found.")
			except Exception as e:
				print(f"An error occurred: {e}")
	