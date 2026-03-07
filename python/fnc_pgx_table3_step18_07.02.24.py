import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# =======================================================
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_SCORED_19643_ST11.txt

prefix1 = "combined_SCORED_"
suffix1 = "_ST11.txt"

prefix2 = "table3_"
suffix2 = "_ST18.txt"

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
                    ls1 = ln1.strip().split(s)
                    brand = ls1[1]
                    brand_str = brand.replace('"', blank)
                    brand_str1 = brand_str.replace(" ", blank)
                    brand_c1 = brand_str1.strip().split(sc)
                    ls3 = [x for x in brand_c1 if len(x) > 4]
                    # print(ls1[0], sn.join(ls3), ls1[2], sep=s)
                    # noinspection PyTypeChecker
                    print(ls1[0], sc.join(ls3), ls1[2], ls1[7], ls1[10], ls1[13], ls1[6], ls1[15], sep=s, file=fileout)

            fileout.close()


pgx_table2(pathx, prefix1, suffix1, prefix2, suffix2)
