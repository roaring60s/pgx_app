import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
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
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_19C_SRT_GTab0_19643_ST8.txt
# /media/p/D11/patients/NARA/MG2401379/asa_7C_combined_19C_MG2401379_ST6.txt

prefix1 = "combined_19C_SRT_GTab0_"
suffix1 = "_ST6.txt"

prefix2 = "table2_final_"
suffix2 = "_ST15.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================

col1 = "DRUG"
col2 = "CATEGORY"
col3 = "GENE"
col4 = "EVIDENCE"
col5 = "EFFECT"
col6 = "GENOTYPE"
col7 = "CLINICAL IMPACT"

#  =========================================================


def pgx_table2(file1, pref1, suf1, pref2, suf2):
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
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split('\t')
                    drug = ls1[0]
                    category = ls1[6]
                    gene = ls1[7]
                    evidence = ls1[10]
                    effect = ls1[13]
                    gt = ls1[16]
                    impact = ls1[17]
                    if int(gt) > 0:
                        print(blank, file=fileout)
                        print(col1, col2, col3, col4, col5, sep=s, file=fileout)
                        print(drug, category, gene, evidence, effect, sep=s, file=fileout)
                        # print(blank, file=fileout)
                        print(col6, col7, sep=s, file=fileout)
                        print(gt, impact, sep=s, file=fileout)
                        # print(blank, blank, sep=sn, file=fileout)

            fileout.close()


pgx_table2(pathx, prefix1, suffix1, prefix2, suffix2)
