import time
import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]

# path1 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/demographics.txt"
# path2 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/sample_4C.txt"
# path3 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/R005_03B_24/biodata/R5.bio.txt"

fileout = open(path3, "w+")

s = "\t"
fd = "/"


def pgx_bio(file1, file2, file_out):
    with open(file1, "r") as p1:
        for ln1 in p1:
            ls1 = ln1.strip().split(s)
            sample1 = ls1[2][1:]
            print(sample1)

            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    sample2 = ls2[0]

                    if sample1 in sample2:
                        print(s.join(ls1), s.join(ls2), sep=s, file=file_out)

    file_out.close()


pgx_bio(path1, path2, fileout)
