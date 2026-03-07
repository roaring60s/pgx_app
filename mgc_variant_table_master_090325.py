import pandas as pd
pd.set_option("display.max_columns", None)

master_ann = "/home/p/mygenics/prj_fgc/anno_hs/variants_excel_anno_UX_090325.txt"
S301 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38_ASA.results_09.03.25_S3O1.txt"
S403 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38.hs.09.03.25.variants.S4O3.txt"
output1 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38.variants_table.txt"
verticals = "/home/p/mygenics/prj_fgc/verticals/vertical_trait_list.txt"

out1 = open(output1, "w+")

df1 = pd.read_csv(master_ann, sep='\t', header=None)
df2 = pd.read_csv(S301, sep='\t', header=None)
df3 = pd.read_csv(S403, sep='\t', header=None)


# print(df2.head(1))

step1 = pd.merge(df1, df2, how="left", left_on=[0, 3], right_on=[10, 4])
columns1 = ['0_x', '1_x', '2_x', '3_x', '4_x', '5_x', '6_x', 31]

step1a = step1[columns1].copy()  # added copy to avoid SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame

step1a.fillna('0/0', inplace=True)

# print(step1a.head(1))

step2 = pd.merge(step1a, df3, how='left', left_on=['0_x', '3_x'], right_on=[0, 3])

columns2 = ['0_x', '1_x', '2_x', '3_x', '4_x', '5_x', '6_x', 31, 6, 7]
step3 = step2[columns2]

step3[7] = step3[7].astype(float).round(4)

dfv = pd.read_csv(verticals, sep='\t', header=None, names=['col1'])

# print(dfv.head(1))

# Create a dictionary to store averages
averages = {}
for unique_string in dfv['col1']:
	matching_rows = step3[step3['0_x'] == unique_string]
	if not matching_rows.empty:
		averages[unique_string] = matching_rows[7].mean()
	else:
		averages[unique_string] = float('nan') # or any other default value if needed

# Create a new column 'average' in df1
step3['average'] = step3['0_x'].map(averages)
#
# Round the average to 4 decimal places
step3['average'] = step3['average'].round(4)

step3.to_csv(out1, sep="\t", index=False, header=False)
