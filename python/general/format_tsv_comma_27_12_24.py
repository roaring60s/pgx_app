
def reformat_tsv(input_file, output_file):
	"""
	Reformats a TSV file by vertically listing comma-separated values in specified columns.
	
	Args:
	input_file: Path to the input TSV file.
	output_file: Path to the output TSV file.
	"""
	try:
		with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
			for line in infile:
				parts = line.strip().split('\t')
				
				# Reformat columns 1, 3 and 6
				for i in [1, 2, 3, 4, 5]:
					if i < len(parts):
						if ',' in parts[i]:
							parts[i] = '"' + '\n'.join(parts[i].split(',')) + '"'
				
				outfile.write('\t'.join(parts) + '\n')
	
	except FileNotFoundError:
		print(f"Error: Input file '{input_file}' not found.")
	except Exception as e:
		print(f"An error occurred: {e}")


# Example usage:
tsv_in = "/media/p/D11/patients/01_report_template/report_lab/TSV1.txt"
tsv_out = "/media/p/D11/patients/01_report_template/report_lab/TSV1_comma_format.txt"


reformat_tsv(tsv_in, tsv_out)
