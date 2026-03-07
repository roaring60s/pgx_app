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
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_CYP2D6_19643_ST2C.txt

prefix1 = "hap_CYP2D6_"
suffix1 = "_ST2C.txt"

prefix2 = "gene_table_input_"
suffix2 = "_ST16.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================


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
                    gene = ls1[0]
                    diplotype = ls1[3]
                    # noinspection PyTypeChecker
                    print(gene, diplotype, sep=s, file=fileout)

            fileout.close()


pgx_table2(pathx, prefix1, suffix1, prefix2, suffix2)
