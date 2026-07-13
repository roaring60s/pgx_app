import time
import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]
dir_path = sys.argv[4]
run = sys.argv[5]

# path1 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/R5.bio.txt"
# path2 = ("/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/data/"
#          "R5.exon9.txt")
# path3 = ("/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/data/"
#          "R5.intron2.txt")
#
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/"

suffix1 = run + "biodata_intermediate_master.txt"
suffix2 = run + ".biodata_master.txt"

path_master = dir_path + suffix1

path_out1 = dir_path + suffix1
fileout1 = open(path_out1, "w+")

path_out2 = dir_path + suffix2
fileout2 = open(path_out2, "w+")

s = "\t"
fd = "/"


def pgx_cnv(file1, file2, file_out):
    with open(file1, "r") as p1:
        for ln1 in p1:
            ls1 = ln1.strip().split(s)
            pgx1 = ls1[2][1:]

            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    pgx2 = ls2[0].split(fd)[1][1:]
                    # pgx2 = pgx2a[1:]
                    result = ls2[5]
                    # print(pgx1, pgx2, result, sep=s)

                    if pgx1 == pgx2:
                        print(pgx1, pgx2, result, sep=s)
                        print(s.join(ls1), result, sep=s, file=file_out)

    file_out.close()


pgx_cnv(path1, path2, fileout1)
time.sleep(5)

pgx_cnv(path_master, path3, fileout2)
