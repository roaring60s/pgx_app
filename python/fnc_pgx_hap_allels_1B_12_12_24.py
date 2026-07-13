import sys

pathx = sys.argv[1]
path1 = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/pgx_asa_hap_alleles_master_05.12.2024.txt"

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
dir_path = sys.argv[3]
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
# /media/p/D11/patients/B016_20240924/asa_7C_hap_19679_ST1A.txt


def match_field(file1, file2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]  # 3 column in biodata
            path_in = dir_path + "hap_" + pgx_idx + "_ST1A.txt"
            path_out = dir_path + "hap_alleles_" + pgx_idx + "_ST1B.txt"
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            path_in_rows = []
            with open(path_in, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    name2 = ls2[1]
                    gt_val = ls2[20]
                    path_in_rows.append((name2, gt_val))

            with open(file2, "r") as p1:
                # score = []
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    hap = ls1[0]
                    name = ls1[1]
                    # name1a = ls1[1].replace('\"', "")
                    name1 = name.split(",")
                    hap_gene = hap.split("*")[0]
                    hap_al = hap.split("*")[1]
                    score = []

                    for name2, gt_val in path_in_rows:
                        for rs in name1:
                            if rs == name2:
                                score.append(gt_val)
                    if len(score) > 0:
                        if any(item == "0" for item in score):
                            # noinspection PyTypeChecker
                            print(s.join(ls1), sp.join(score), hap_gene, hap_al, "*1/*1", sep=s, file=fileout)
                            # score.clear()
                        if all(item != "0" for item in score) and any(item != "2" for item in score):
                            # noinspection PyTypeChecker
                            print(s.join(ls1), sp.join(score), hap_gene, hap_al, "*1/*" + hap_al, sep=s, file=fileout)
                            # score.clear()
                        if all(item == "2" for item in score):
                            # noinspection PyTypeChecker
                            print(s.join(ls1), sp.join(score), hap_gene, hap_al, "*" + hap_al + "/*" + hap_al,
                                  sep=s, file=fileout)
                            # score.clear()

        fileout.close()


match_field(pathx, path1)
