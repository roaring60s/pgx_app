import sys

pathx = sys.argv[1]
path1 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path1 = ("/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/"
#          "pgx_asa_var_clin_alleles_EV12_master_UX_03.02.24.txt")
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

# Variant Clinical Alleles Annotation
# Below is a sample input file
# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_var_19641.txt

prefix1 = "var_"

prefix2 = "var_CLIN_"
suffix2 = "_ST3.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# =========================================================
# sample file
id1 = 2  # C => RSID
id2 = 16  # Q => GT in 0/1
# pgx_asa_var_clin_alleles_EV12_master_UX_03.02.24.txt
id3 = 1  # B => RSID
id4 = 26  # AA => GT in 0/1
# =========================================================


def matching_files(file1, file2, no1, no2, no3, no4):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix1 + pgx_idx
            path_out = dir_path + prefix2 + pgx_idx + suffix2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)    
    
            with open(path_in, "r")as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split('\t')
                    var1 = ls1[no1]  # RSID
                    gt1 = ls1[no2]  # GT
        
                    with open(file2, "r")as p2:
                        for ln2 in p2:
                            ls2 = ln2.strip().split('\t')
                            var2 = ls2[no3]  # RSID
                            gt2 = ls2[no4]  # GT
        
                            if var1 == var2 and gt1 == gt2:
                                print(s.join(ls1), s.join(ls2), sep="\t", file=fileout)
                            
    fileout.close()


matching_files(pathx, path1, id1, id2, id3, id4)
