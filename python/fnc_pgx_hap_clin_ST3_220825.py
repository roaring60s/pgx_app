import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = ("/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/"
#          "pgx_asa_hap_clin_alleles_EV13_master_UX_03.02.24.txt")
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# Clinical Alleles Annotation of Haplotypes
# Below is a sample input file
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_SPLIT_19643_ST2E.txt

prefix1 = "hap_SPLIT_"
suffix1 = "_ST2E.txt"

prefix2 = "hap_CLIN_"
suffix2 = "_ST3.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================
# sample file
id1 = 5
id2 = 6
#  pgx_asa_hap_clin_alleles_EV13_master_UX_03.02.24.txt
id3 = 1  # haplotype => Cell B


def matching_files(file1, file2, no1, no2, no3):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            path_in = dir_path + prefix1 + pgx_idx + suffix1
            path_out = dir_path + prefix2 + pgx_idx + suffix2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            # opening clinical annotation master file
            ref_index = {}
            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    hap2 = ls2[no3].strip()
                    effect = ls2[11]
                    ref_index.setdefault(hap2, []).append((effect, ls2))

            # opening sample files
            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    hap1 = ls1[no1]
                    gt1 = ls1[no2]
                    eff_value = "Normal function"

                    # amended to exclude Normal function
                    for effect, ls2 in ref_index.get(hap1, []):
                        if int(gt1) > 0:
                            if effect != eff_value:
                                print(s.join(ls1), s.join(ls2), sep="\t", file=fileout)

        fileout.close()


matching_files(pathx, path1, id1, id2, id3)
