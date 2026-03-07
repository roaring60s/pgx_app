
import sys

path1 = sys.argv[1]
path2 = sys.argv[2]
path3 = sys.argv[3]
path_out = sys.argv[4]

# path1 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path2 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_208084170002.txt"
# path3 = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_207408230011.txt"

#  Function to select sample's rows from ASA file using mgrs id from biodata files.
#  The Function checks the biodata for corrects ASA file to be used

s = "\t"
sb = ""
sp = ","
# directory for the outfile
# path_out = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C"
# sample mgrc id in file 1 => biodata
fd1 = 13
# sample pgx id in file 1 => biodata
fd2 = 2
# sample asa file name in file 1 => biodata
fd3 = 16
# sample mgrc id in files 2 and 3 => ASA files 2 and 3
fd4 = 1


def fnc_sample_from_asa(file1, file2, file3, out, no1, no2, no3, no4):
    with open(file1, "r")as p1:
        for ln1 in p1:
            ls1 = ln1.strip().split(s)
            mgrc_id1 = ls1[no1]
            asa_name = ls1[no3].split("_")[1]
            pgx_id1 = ls1[no2]
            path5 = out + pgx_id1
            outfile = open(path5, "w+")
            print(pgx_id1, asa_name, mgrc_id1, sep=s)

            if asa_name in path2:
                with open(file2, "r")as p2:
                    for ln2 in p2:
                        ls2 = ln2.strip().split(s)
                        mgrc_id2 = ls2[no4]
                        if mgrc_id1 == mgrc_id2:
                            print(s.join(ls2), sep=s, file=outfile)

                # outfile.close()

            if asa_name in path3:
                with open(file3, "r")as p3:
                    for ln3 in p3:
                        ls3 = ln3.strip().split(s)
                        mgrc_id3 = ls3[no4]
                        if mgrc_id1 == mgrc_id3 and pgx_id1 != ".":
                            print(s.join(ls3), sep=s, file=outfile)

    outfile.close()


fnc_sample_from_asa(path1, path2, path3, path_out, fd1, fd2, fd3, fd4)
