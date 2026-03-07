import csv
import re
import os


def natural_sort_key(haplotype):
	"""
	Parses a haplotype string like '*12A' into a sortable tuple: (12, 'A').
	This ensures *5 comes before *12.
	"""
	# Remove the '*' and split into numeric and alphabetic parts
	match = re.search(r'(\d+)([A-Z]*)', haplotype)
	if match:
		number = int(match.group(1))  # Convert '12' to 12
		suffix = match.group(2)  # 'A'
		return (number, suffix)
	return (0, haplotype)  # Fallback for unexpected formats


def sort_diplotypes_naturally(diplotype_str):
	"""
	Sorts diplotypes by hap1 then hap2 using natural numeric logic.
	"""
	if not diplotype_str:
		return ""
	
	# Split by pipe and remove empty strings/whitespace
	raw_diplotypes = [d.strip() for d in diplotype_str.split('|') if d.strip()]
	
	# Sort using a custom key that handles numeric star alleles
	sorted_list = sorted(
		raw_diplotypes,
		key=lambda diplotype: [
			natural_sort_key(hap.strip()) for hap in diplotype.split('/')
		]
	)
	
	return " | ".join(sorted_list)


def process_gene_table(input_path):
	base, ext = os.path.splitext(input_path)
	output_path = f"{base}_final_sorted{ext}"
	
	try:
		with open(input_path, mode='r', encoding='utf-8', newline='') as infile:
			reader = csv.DictReader(infile, delimiter='\t')
			fieldnames = reader.fieldnames
			
			processed_rows = []
			for row in reader:
				if 'HAP' in row and row['HAP']:
					row['HAP'] = sort_diplotypes_naturally(row['HAP'])
				processed_rows.append(row)
		
		with open(output_path, mode='w', encoding='utf-8', newline='') as outfile:
			writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter='\t')
			writer.writeheader()
			writer.writerows(processed_rows)
		
		print(f"Success! Natural sorting applied. Created: {output_path}")
	
	except Exception as e:
		print(f"An error occurred: {e}")


if __name__ == "__main__":
	target_file = "/media/D1/patients/2026/MGRC_20260305/final/asa_gene_table_final_022128_ST17.txt"
	process_gene_table(target_file)
