
import time
import sys
import fnc_pgx_table1_replace_comma_28_12_24

pathx = sys.argv[1]
path1 = sys.argv[2]
path2 = sys.argv[3]
dir_path = sys.argv[4]

# pathx = ("/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/01A_24/biodata/"
#          "mgrc_biodata_HS00010001_HS04083572_12C_V1.txt")
# path1 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/pgx_asa_atcl5_dx_table_ev_ab4_30.01.2024.txt"
# path2 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/atc_1level_codes.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_"

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
#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_SCORED_19643_ST11.txt

prefix1 = "combined_SCORED_"
suffix1 = "_ST11.txt"

prefix2 = "table1_"
suffix2 = "_ST12.txt"

prefix3 = "table1_"
suffix3 = "_ST13.txt"

prefix4 = "table1_"
suffix4 = "_ST14.txt"

prefix5 = "table1_final_"
suffix5 = "_ST15.txt"


#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
# ===========================================================


def select_columns_S12(file1, pref1, pref2, suf1, suf2):
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

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    # noinspection PyTypeChecker
                    print(ls1[0], ls1[1], ls1[2], ls1[14], ls1[3], ls1[4], ls1[5], ls1[6], ls1[15], sep=s, file=fileout)

        fileout.close()


def func_table1_S13(file1, file2, pref1, pref2, suf1, suf2):
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

            drug_category_index = {}
            with open(path_in, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    drug = ls2[3]
                    category = int(ls2[8])
                    drug_category_index.setdefault(drug, []).append(category)

            with open(file2, "r")as p1:
                for ln1 in p1:
                    level1 = []
                    level2 = []
                    level3 = []
                    ls1 = ln1.strip().split(s)
                    atc5 = ls1[0]
                    act5_name = ls1[1]
                    drug_list = ls1[2].strip().split(sc)
                    drug_list1 = ls1[2].strip().split(sc)

                    for item in drug_list1:
                        drug = item
                        for category in drug_category_index.get(item, []):
                            if category == 1:
                                level1.append(item.title())
                                if drug in drug_list:
                                    drug_list.remove(item)
                            if category == 2:
                                level2.append(item.title())
                                if drug in drug_list:
                                    drug_list.remove(item)
                            if category == 3:
                                level3.append(item.title())
                                if drug in level2:
                                    level2.remove(item)
                                if drug in drug_list:
                                    drug_list.remove(item)

                    x = sorted(drug_list)
                    level1.sort()
                    level2.sort()
                    level3.sort()
                    # noinspection PyTypeChecker
                    print(atc5, act5_name, sc.join(x), sc.join(level1), sc.join(level2), sc.join(level3), sep=s, file=fileout)

            fileout.close()


def fnc_table1_st14(file1, file2, pref1, suf1, pref2, suf2):
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

            atc_index = {}
            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split('\t')
                    atc2 = ls2[0]
                    name2 = ls2[1].upper()
                    atc_index.setdefault(atc2, []).append(name2)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split('\t')
                    atc1 = ls1[0][0]
                    splice1 = len(ls1)
                    name1 = ls1[1]
                    green = ls1[2].title()

                    for name2 in atc_index.get(atc1, []):
                        # noinspection PyTypeChecker
                        print(name2, name1, green, s.join(ls1[3: splice1]), sep=s, file=fileout)

            fileout.close()


print(f"Processing Step 12: Selecting Columns for Processing")


select_columns_S12(pathx, prefix1, prefix2, suffix1, suffix2)
time.sleep(10)

print(f"Processing Step 13: Assigning Drugs to Clinical Effect Groups")


func_table1_S13(pathx, path1, prefix2, prefix3, suffix2, suffix3)
time.sleep(10)

print(f"Processing Step 14: Adding ATC Level 1 Name")


fnc_table1_st14(pathx, path2, prefix3, suffix3, prefix4, suffix4)

print(f"Processing Step 15: Formatting Comma")


fnc_pgx_table1_replace_comma_28_12_24.reformat_tsv(pathx, dir_path, prefix4, suffix4, prefix5, suffix5)
