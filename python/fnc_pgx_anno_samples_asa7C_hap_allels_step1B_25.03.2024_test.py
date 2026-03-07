import sys
import csv

# pathx = sys.argv[1]
# path1 = sys.argv[2]

pathx = "/media/p/D11/patients/B020_20241127/biodata/R20.biodata_master.txt"
path1 = "/home/p/mygenics/pgx_app/annotation/pgx_asa_hap_alleles_master_05.01.2024.txt"

# Function to generate final results for haplotypes that can be used for selection of drugs and clinical annotation.
#
s = "\t"
# sb = ""
sp = ","

'''
---------------------------------------------------------
file name template
/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_hap_19715_ST1A.txt

asa_7C_hap_19643_ST1A.txt

'''
# ========================================================
# directory for the in and out-file
# dir_path = sys.argv[3]
dir_path = "/media/p/D11/patients/B020_20241127/asa_7C_"
#  ========================================================
#  pgx name in biodata file
fd0 = 2
#  =========================================================
# name (asa rsid) in hap master file
fd1 = 0
# asa fwd ref in hap master file
fd2 = 1
# ==========================================================
# name (asa rsid) in sample file
fd3 = 1
# asa fwd al1 in sample file
fd4 = 20
# ===========================================================
'''
st1 = ".1"
st2 = ".2"
rgt = {"T": "A", "A": "T", "C": "G", "G": "C", "D": "I", "I": "D"}
snp_gt = snp[0:3:2]
'''


def match_field(file1, file2, no0, no1, no2, no3, no4):
	unique_rows = set()
	with open(file1, "r")as px:
		counter = 0
		for lnx in px:
			counter = counter + 1
			lsx = lnx.strip().split("\t")
			pgx_idx = lsx[no0]
			# asa_7C_020450_TEST.txt
			path_in = dir_path + "hap_" + pgx_idx + "_TEST.txt"
			path_out = dir_path + "hap_alleles_" + pgx_idx + "_TEST.txt"
			fileout = open(path_out, "w+")
			print(counter, pgx_idx, sep=s)

			with open(file2, "r") as p1:
				# score = []
				for ln1 in p1:
					ls1 = ln1.strip().split(s)
					hap = ls1[no1]
					name = ls1[no2]
					name1a = ls1[no2].replace('\"', "")
					name1 = name1a.split(sp)
					hap_gene = hap.split("*")[0]
					hap_al = hap.split("*")[1]
					score = []

					with open(path_in, "r") as p2:
						for ln2 in p2:
							ls2 = ln2.strip().split(s)
							name2 = ls2[no3]
							gt_val = ls2[no4]

							# if len(name1) == 1:
							#     # print(name1, name2, gt_val, sep=s)
							#     if name == name2:
							#         # print(name2, gt_val, sep=s)
							#         if int(gt_val) == 0:
							#             print(s.join(ls1), gt_val, hap_gene, hap_al, "*1/*1", sep=s, file=fileout)
							#         if gt_val == "1":
							#             print(s.join(ls1), gt_val, hap_gene, hap_al, "*1/*" + hap_al, sep=s,
							#                   file=fileout)
							#         if gt_val == "2":
							#             print(s.join(ls1), gt_val, hap_gene, hap_al, "*" + hap_al + "/*" + hap_al,
							#                   sep=s, file=fileout)
							#
							# if len(name1) > 1:
							for rs in name1:
								if rs == name2:
									score.append(gt_val)
						new_data = []
						# processed_data.append(tsv2_row + [G1, S1])
						if any(item == "0" for item in score):
							new_data.append(s.join(ls1) + sp.join(score) + hap_gene + hap_al + "*1/*1")
							# score.clear()
						if all(item != "0" for item in score) and any(item != "2" for item in score):
							new_data.append(s.join(ls1) + sp.join(score) + hap_gene + hap_al + "*1/*" + hap_al)
							# score.clear()
						if all(item == "2" for item in score):
							new_data.append(s.join(ls1) + sp.join(score) + hap_gene + hap_al + "*" + hap_al + "/*" + hap_al)
							# score.clear()

						new_data = list(set(tuple(row) for row in new_data))

						# Sort by column 1
						new_data.sort(key=lambda x: x[0])

						print(s.join(new_data), file=fileout)

						# with open(path_out, 'w+', newline='') as f:
						# 	writer = csv.writer(f, delimiter='\t')
						# 	writer.writerows(new_data)

	fileout.close()


match_field(pathx, path1, fd0, fd1, fd2, fd3, fd4)
