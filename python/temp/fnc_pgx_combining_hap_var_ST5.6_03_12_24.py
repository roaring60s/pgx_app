
import time
import sys
import csv
pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# Drug Annotation of Haplotypes with Clinical Anno.
# Below is a sample input files
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_var_CLIN_DRG_19643_ST4.txt
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_CLIN_DRG_19643_ST4.txt


prefix1 = "hap_CLIN_DRG_"
suffix1 = "_ST4.txt"

suffix2 = "_ST5.txt"

prefix3 = "var_CLIN_DRG_"

prefix4 = "combined_19C_"
suffix3 = "_ST6.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================
# id1 = 18  # S => Drug Evidence in a sample HAP file
# id2 = 29  # AD => Drug Evidence in a sample VAR file
# fnc_selecting19C_stp5(pathx, prefix1, suffix1, suffix2, id1)
# /media/p/D11/patients/B020_20241127/asa_7C_hap_CLIN_DRG_020450_ST4.txt


def fnc_hap_selecting19C_stp5(file1, pd1, s1, s2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            pr1 = pd1
            su1 = s1
            su2 = s2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr1 + pgx_idx + su2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    # dev = ls1[18].strip()   # S => drug evidence in sample file

                    if len(ls1) == 46:
                        # print(ls1[0])
                        # evidence level set above 4 for haplotypes
                        if ls1[18] != "4":
                            # print(ls1[0])
                            print(ls1[0], ls1[2], ls1[3], ls1[4], ls1[5], ls1[6], ls1[7], ls1[8], ls1[13], ls1[14], ls1[18], ls1[19], ls1[20], ls1[21], ls1[22], ls1[23], ls1[24], ls1[25], sep=s, file=fileout)

        # fileout.close()


def fnc_var_selecting19C_stp5(file1, pd1, s1, s2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            pr1 = pd1
            su1 = s1
            su2 = s2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr1 + pgx_idx + su2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)

                    if len(ls1) == 53:
                        # evidence level set above 4 for variants
                        if ls1[29] != "4":
                            print(ls1[0], ls1[2], ls1[3], ls1[4], ls1[5], ls1[6], ls1[7], ls1[28], ls1[27], ls1[25], ls1[29], ls1[30], ls1[31], ls1[32], ls1[33], ls1[34], ls1[35], ls1[36], sep=s, file=fileout)

        fileout.close()


def fnc_combine_files(file1, pref1, pref2, pref3, suf1, suf2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            pr1 = pref1
            pr2 = pref2
            pr3 = pref3
            su1 = suf1
            su2 = suf2
            file_var = dir_path + pr1 + pgx_idx + su1
            file_hap = dir_path + pr2 + pgx_idx + su1
            file_combined = dir_path + pr3 + pgx_idx + "sorting.txt"
            file_sorted = dir_path + pr3 + pgx_idx + su2
            # files = [file_var, file_hap]
            print(counter, pgx_idx, sep=s)

            combine_and_filter_tsv(file_var, file_hap, file_combined, file_sorted)


def combine_and_filter_tsv(tsv1_path, tsv2_path, tsv3_path, tsv4_path):
    """
    Combines two TSV files, removes rows with "." in the 4th column,
    and sorts the result by the 1st column.

    Args:
      tsv1_path: Path to the first TSV file.
      tsv2_path: Path to the second TSV file.
      tsv3_path: Path to save the combined and filtered TSV file.
      tsv4_path: Path to save the sorted TSV file.
    """

    with open(tsv1_path, 'r', newline='') as f1, \
         open(tsv2_path, 'r', newline='') as f2, \
         open(tsv3_path, 'w', newline='') as f3:

        reader1 = csv.reader(f1, delimiter='\t')
        reader2 = csv.reader(f2, delimiter='\t')
        writer = csv.writer(f3, delimiter='\t')

        # Combine TSV1 and TSV2 into TSV3
        for row in reader1:
            writer.writerow(row)
        for row in reader2:
            writer.writerow(row)

    with open(tsv3_path, 'r', newline='') as f3, \
         open(tsv4_path, 'w', newline='') as f4:

        reader = csv.reader(f3, delimiter='\t')
        writer = csv.writer(f4, delimiter='\t')

        # Filter rows with "." in the 4th column and sort by the 1st column
        filtered_data = [row for row in reader if row[3] != "."]
        sorted_data = sorted(filtered_data, key=lambda row: row[0])

        for row in sorted_data:
            writer.writerow(row)


fnc_hap_selecting19C_stp5(pathx, prefix1, suffix1, suffix2)
time.sleep(5)


fnc_var_selecting19C_stp5(pathx, prefix3, suffix1, suffix2)
time.sleep(5)

fnc_combine_files(pathx, prefix3, prefix1, prefix4, suffix2, suffix3)
