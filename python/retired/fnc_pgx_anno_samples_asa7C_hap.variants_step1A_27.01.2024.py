import sys

pathx = sys.argv[1]
path1 = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/pgx_asa_hap_snps_master_05.01.2024.txt"

s = "\t"
sb = ""
sp = ","
'''
mgrc_biodata_HS00010001_HS04083572_12C_V1.txt file fields:
A / 0 => mgrc id
F / 5 => patient name
I / 8 => ASA file name
J / 9 => pgx id
K / 10 => exon 9 result
L / 11 => intron 2 result (end of fields)

pgx_asa_hap_snps_master_05.01.2024.txt file fields:
ASA RSID Name   J   9
ASA REF         R   17
ASA ALT         S   18
'''
# ========================================================
# directory for the in and out-file
dir_path = sys.argv[3]
#  ========================================================
#  pgx name in biodata file is field 9 = fd1

# name (asa rsid) in hap master file
fd1 = 9
# asa fwd ref in hap master file
fd2 = 17
# asa fwd alt in hap master file
fd3 = 18
#  =========================================================
# name (asa rsid) in sample file
fd4 = 0
# asa fwd al1 in sample file
fd5 = 5
# asa fwd al2 in sample file
fd6 = 6
# ===========================================================
# str1 = "+"
# str2 = "-"
# rgt = {"T": "A", "A": "T", "C": "G", "G": "C", "D": "I", "I": "D"}
# snp_gt = snp[0:3:2]


def pgx_hap_step1A(file1, file2, no2, no3, no4, no5, no6):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            # MGRC sample number for PGX report
            pgx_idx = lsx[2]
            path_in = dir_path + pgx_idx
            path_out = dir_path + "hap_" + pgx_idx + "_ST1A.txt"
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(file2, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split("\t")
                    # ASA name of RSID
                    name1 = ls1[9]
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


pgx_hap_step1A(pathx, path1, fd2, fd3, fd4, fd5, fd6)
