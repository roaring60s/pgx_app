import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/pgx_asa_variants_snps_master_05.01.2024.txt"

s = "\t"
# sb = ""
# sp = ","
'''
The Biodata file fields are as follows:
A / 0 => mgrc id
F / 5 => patient name
I / 8 => ASA file name
J / 9 => pgx id
K / 10 => exon 9 result
L / 11 => intron 2 result (end of fields)
'''
# ========================================================
# directory for the in and out-file
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02C_24/
#  ========================================================
# name (asa rsid) in variant master file
fd1 = 6
# asa fwd ref in variant master file
fd2 = 14
# asa fwd alt in variant master file
fd3 = 15
#  =========================================================
# # name (asa rsid) in hap master file
# fd1 = 9
# # asa fwd ref in hap master file
# fd2 = 17
# # asa fwd alt in hap master file
# fd3 = 18
# ==========================================================
# name (asa rsid) in sample file
fd4 = 0
# asa fwd al1 in sample file
fd5 = 5
# asa fwd al2 in sample file
fd6 = 6
# asa fwd al2 in sample file
fd7 = 2
# ===========================================================
# str1 = "+"
# str2 = "-"
# rgt = {"T": "A", "A": "T", "C": "G", "G": "C", "D": "I", "I": "D"}
# snp_gt = snp[0:3:2]


def pgx_var_step1(file1, file2, no1, no2, no3, no4, no5, no6, no7):
    with open(file1, "r")as px:
        for lnx in px:
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[no7]
            path_in = dir_path + pgx_idx
            path_out = dir_path + "var_" + pgx_idx
            fileout = open(path_out, "w+")

            with open(file2, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split("\t")
                    name1 = ls1[no1]
                    ref1 = ls1[no2]
                    alt1 = ls1[no3]
                    gt00 = "0/0"
                    gt01 = "0/1"
                    gt11 = "1/1"

                    with open(path_in, "r") as p2:
                        for ln2 in p2:
                            ls2 = ln2.strip().split("\t")
                            name2 = ls2[no4]
                            al1 = ls2[no5]
                            al2 = ls2[no6]

                            if name1 == name2:
                                if al1 == "-" and al2 == "-":
                                    continue

                                if al1 == al2 and al1 == ref1:
                                    # noinspection PyTypeChecker
                                    print(s.join(ls1), gt00, 0, sep="\t", file=fileout)
                                if al1 == al2 and al1 == alt1:
                                    # noinspection PyTypeChecker
                                    print(s.join(ls1), gt11, 2, sep="\t", file=fileout)
                                if al1 != al2:
                                    # noinspection PyTypeChecker
                                    print(s.join(ls1), gt01, 1, sep="\t", file=fileout)

            fileout.close()


pgx_var_step1(pathx, path1, fd1, fd2, fd3, fd4, fd5, fd6, fd7)
