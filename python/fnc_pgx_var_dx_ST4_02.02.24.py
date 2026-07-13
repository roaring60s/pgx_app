import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/drugs_ann_cln.ann_EV13_ATC12_30.01.24.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# Variant Clinical Alleles Annotation
# Below is a sample input file
# /media/p/D11/patients/B020_20241127/asa_7C_hap_CLIN_020773_ST3.txt


prefix1 = "var_CLIN_"
suffix1 = "_ST3.txt"

prefix2 = "var_CLIN_DRG_"
suffix2 = "_ST4.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================
#  sample file
id1 = 25  # Z => drug name
# master file
id2 = 1  # B => drug name


def matching_files(file1, file2, no1):
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

            # opening master annotation file
            drug_index = {}
            with open(file2, "r")as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    dx2 = ls2[1].strip()  # Drug name
                    dx2C = ls2[2]  # drug name with capital first character
                    brand = ls2[2]  # trade name
                    code = ls2[31]  # ATC Code
                    atc_l1code = ls2[25]
                    atc_l1name = ls2[26]
                    atc_l2code = ls2[27]
                    atc_l2name = ls2[28]
                    drug_index.setdefault(dx2, []).append(
                        (dx2C, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name)
                    )

            # opening sample files
            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    dx1 = ls1[no1].strip()  # drug name in sample file

                    for dx2C, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name in drug_index.get(dx1, []):
                        # noinspection PyTypeChecker
                        print(dx2C, dx1, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name,
                              s.join(ls1), sep=s, file=fileout)
                    
        fileout.close()


matching_files(pathx, path1, id1)
