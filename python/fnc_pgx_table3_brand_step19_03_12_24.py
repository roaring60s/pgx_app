import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "R2_biodata_master.txt"
# path1 = "pgx_brand_names_R2_UX_11.02.24.txt"
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

# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_table3_final_19719_ST18.txt

prefix1 = "table3_"
suffix1 = "_ST18.txt"

prefix2 = "table3_Brand_"
suffix2 = "_ST19.txt"

prefix3 = "table3_Brand_"
suffix3 = "_ST20.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
# ===========================================================


def pgx_table2(file1, file2, pref1, suf1, pref2, suf2):
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

            with open(file2, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    drug1 = ls1[0].strip()
                    brand1 = ls1[1]

                    with open(path_in, "r")as p2:
                        for ln2 in p2:
                            ls2 = ln2.strip().split(s)
                            drug2 = ls2[0].strip()
                            atc = ls2[2]
                            # gene = ls2[3]
                            # evidence = ls2[4]
                            effect2 = ls2[5].replace(';', ',')
                            effect1 = effect2.strip().split(",")
                            effect = list(set(effect1))
                            clin_group = ls2[6]
                            score = ls2[7]

                            # brand2 = ls2[1].replace('"', "")

                            if drug1 == drug2:
                                # noinspection PyTypeChecker
                                print(drug1, brand1, atc, ",".join(effect), clin_group, score, sep=s, file=fileout)

            fileout.close()


def sort_tsv(file1, pref2, suf2, pref3, suf3):
    with open(file1, "r") as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            pr2 = pref2
            pr3 = pref3
            su2 = suf2
            su3 = suf3
            path_in = dir_path + pr2 + pgx_idx + su2
            path_out = dir_path + pr3 + pgx_idx + su3
            # fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            """
            Sorts a TSV file by the first column and then the sixth column.
        
            Args:
                input_filename (str): The name of the input TSV file.
                output_filename (str): The name of the output TSV file.
            """

            with open(path_in, 'r') as infile:
                lines = [line.strip().split('\t') for line in infile]

            # Sort by first column, then sixth column
            # Sort by first column, then sixth column in reverse
            # lines.sort(key=lambda x: (x[ 0 ], -int(x[ 5 ])))  # Note the -int(x[5])
            lines.sort(key=lambda x: (-int(x[5]), x[0]))

            with open(path_out, 'w+') as outfile:
                for line in lines:
                    outfile.write('\t'.join(line) + '\n')


pgx_table2(pathx, path1, prefix1, suffix1, prefix2, suffix2)


sort_tsv(pathx, prefix2, suffix2, prefix3, suffix3)
