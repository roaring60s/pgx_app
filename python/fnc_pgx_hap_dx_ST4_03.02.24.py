import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "R.biodata_master.txt"
# path1 = "/home/p/mygenics/pgx_app/ann/drugs_cln_ann_EV13_ATC13_UX_230125.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# Drug Annotation of Haplotypes with Clinical Anno.
# Below is a sample input file
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_CLIN_19643_ST3.txt

# /media/p/D11/patients/B020_20241127/asa_7C_hap_CLIN_020773_ST3.txt

prefix1 = "hap_CLIN_"
suffix1 = "_ST3.txt"

prefix2 = "hap_CLIN_DRG_"
suffix2 = "_ST4.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================


def matching_files(file1, file2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix1 + pgx_idx + suffix1
            path_out = dir_path + prefix2 + pgx_idx + suffix2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            drug_index = {}
            with open(file2, "r")as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split('\t')
                    dx2 = ls2[1].strip()  # B => Drug name
                    dx2C = ls2[2]  # Drug name with capital first character
                    brand = ls2[4]  # trade name
                    code = ls2[31]  # ATC drug code
                    atc_l1code = ls2[25]
                    atc_l1name = ls2[26]
                    atc_l2code = ls2[27]
                    atc_l2name = ls2[28]
                    drug_index.setdefault(dx2, []).append(
                        (dx2C, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name)
                    )

            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split('\t')
                    dx1 = ls1[14].strip()   # Drug name in sample file

                    for dx2C, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name in drug_index.get(dx1, []):
                        # noinspection PyTypeChecker
                        print(dx2C, dx1, brand, code, atc_l1code, atc_l1name, atc_l2code, atc_l2name,
                              s.join(ls1), sep="\t", file=fileout)
                    
        fileout.close()


matching_files(pathx, path1)
