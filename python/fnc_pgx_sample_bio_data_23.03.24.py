import sys

path1 = sys.argv[1]
dir_path = sys.argv[2]
report_date = sys.argv[3]
report_date1 = sys.argv[4]

# path1="/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/R5_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/"

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

# prefix1 = "hap_CYP2D6_"
# suffix1 = "_ST2C.txt"

prefix2 = "demographics_table_final_"
suffix2 = "_ST17.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
sn = "\n"
blank = ""
dash = "_"
hyphen = "-"
test = "PGX03"
# ===========================================================


def pgx_demo(file1, pref2, suf2):
    with open(file1, "r") as p1:
        counter = 0
        for ln1 in p1:
            counter = counter + 1
            ls1 = ln1.strip().split(s)
            pgx = ls1[2]
            path_out = dir_path + pref2 + pgx + suf2
            fileout = open(path_out, "w+")
            print(counter, pgx, sep=s)

            acc1 = ls1[0].split(sf)
            acc = dash.join(acc1)
            account = ls1[0]
            name = ls1[1]
            specimen = ls1[3]
            dob = ls1[6]
            gender = ls1[7]
            coll_date = ls1[10]
            receive_date = ls1[11]
            report = report_date
            report1 = report_date1
            clinic = ls1[4]
            physician = ls1[5]

            print(blank, file=fileout)
            print(name, file=fileout)
            print(account, file=fileout)
            print(pgx, file=fileout)
            print(dob, file=fileout)
            print(gender, file=fileout)
            print(blank, file=fileout)
            print(specimen, file=fileout)
            print(coll_date, file=fileout)
            print(receive_date, file=fileout)
            print(report1, file=fileout)
            print(blank, file=fileout)
            print(physician, file=fileout)
            print(clinic, file=fileout)

            print(blank, file=fileout)
            print(acc + hyphen + report, file=fileout)

    fileout.close()


pgx_demo(path1, prefix2, suffix2)
