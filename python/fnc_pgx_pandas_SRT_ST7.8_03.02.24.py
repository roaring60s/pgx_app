import pandas as pd
import time
import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_19C_19643_ST6.txt

prefix1 = "combined_19C_"
suffix1 = "_ST6.txt"

prefix2 = "combined_19C_SRT_"
suffix2 = "_ST7.txt"

prefix3 = "combined_19C_SRT_"
suffix3 = "_ST8.txt"

idx1 = 9

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================


def fnc_pandas_sort_stp7(file1, pd1, pd2, s1, s2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            pr1 = pd1
            pr2 = pd2
            su1 = s1
            su2 = s2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr2 + pgx_idx + su2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as x:
                df = pd.read_table(x, names=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])
                result1 = df.sort_values(1)
                result = result1[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]].drop_duplicates()
                result.to_csv(fileout, sep=s, index=False, header=False)


def fnc_pandas_sortGTab0_stp8(file1, pd1, pd2, s1, s2, no1):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            pr1 = pd1
            pr2 = pd2
            su1 = s1
            su2 = s2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr2 + pgx_idx + su2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    gt = ls1[no1].strip()   # R => GT score in sample file

                    if int(gt) > 0:
                        print(s.join(ls1), file=fileout)

        fileout.close()


fnc_pandas_sort_stp7(pathx, prefix1, prefix2, suffix1, suffix2)
time.sleep(10)

fnc_pandas_sortGTab0_stp8(pathx, prefix2, prefix3, suffix2, suffix3, idx1)
