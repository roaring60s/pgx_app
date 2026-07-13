
import os

pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"

path1 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/mgrc_biodata_02A_NB.txt"

# Function to create separate folders for each patient using Biodata file
#
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
'''
# ========================================================

dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/"
run_name1 = "01A_24/"
run_name2 = "02A_24/"
run_path1 = dir_path + run_name1
run_path2 = dir_path + run_name2

#  ========================================================
#  pgx name in biodata file
fd0 = 2
fd1 = 3
#  =========================================================


def match_field(file1, path, no0):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[no0]
            path_in = path + pgx_idx
            print(counter, pgx_idx, sep=s)

            if pgx_idx.isdigit() == True:

                if not os.path.exists(path_in):
                    os.makedirs(path_in)


# match_field(pathx, run_path1, fd0)

match_field(path1, run_path2, fd1)
