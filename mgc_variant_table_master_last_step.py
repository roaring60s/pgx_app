import pandas as pd
pd.set_option("display.max_columns", None)

S710 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38.hs.09.03.25.summary_results.sorted.S7O10.txt"
input1 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38.variants_table.txt"
output2 = "/media/p/D11/patients/B000_nara/MG2500214/MG2500214.38.variants_table.txt_final.txt"

out2 = open(output2, "w+")

df4 = pd.read_csv(S710, sep='\t', header=None)

step4 = pd.read_csv(input1, sep='\t', header=None)

# print(step4.head(1))

step5 = pd.merge(step4, df4, how='left', left_on=0, right_on=6)
# print(step5.head(10))

columns3 = ['0_x', '1_x', '2_x', '3_x', '4_x', '5_x', '6_x', '7_x', '8_x', '9_x', '10_x', '1_y', 14]
step6 = step5[columns3]

step6.to_csv(out2, sep="\t", index=False, header=False)
