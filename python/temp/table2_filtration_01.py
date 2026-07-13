def filter_tsv(tsv1_file, tsv2_file, tsv3_file, cols_to_save):
    """
    Filters TSV1 based on values in TSV2 and saves specific columns to TSV3.

    Args:
      tsv1_file: Path to the first TSV file.
      tsv2_file: Path to the second TSV file.
      tsv3_file: Path to the output TSV file.
      cols_to_save: A list of column indices (starting from 0) to save in TSV3.
    """

    with open(tsv1_file, 'r') as f1, open(tsv2_file, 'r') as f2:
        tsv1_data = [line.strip().split('\t') for line in f1]
        tsv2_data = [line.strip().split('\t') for line in f2]

    # Extract values from column 3 of TSV2
    tsv2_col3_values = [row[2] for row in tsv2_data]

    filtered_data = []
    for row in tsv1_data:
        if row[0] in tsv2_col3_values:  # Check if column 1 of TSV1 matches any value in column 3 of TSV2
            filtered_data.append(row)

    with open(tsv3_file, 'w') as f3:
        for row in filtered_data:
            selected_cols = [row[i] for i in cols_to_save]
            f3.write('\t'.join(selected_cols) + '\n')


# Example usage:
filter_tsv('tsv1.tsv', 'tsv2.tsv', 'tsv3.tsv', [1, 4, 2, 0])  # Save columns 2, 5, 3, and 1
