import sys
import time

pathx = sys.argv[1]
path2 = sys.argv[2]
dir_path = sys.argv[3]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# path2 = "/home/p/mygenics/01_system.development/01_PGX/sys/master_tables/pgx_hap_genes_1C_SRT_DD_UX.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

'''
asa_7C_hap_alleles file fields:
D / 3 => Gene
F / 5 => haplotype 
'''

# ========================================================
# directory for the in and out-file
#  Full path:
#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/asa_7C_hap_alleles_19715_ST1B.txt

prefix1 = "hap_alleles_"
suffix1 = "_ST1B.txt"

prefix2 = "hap_diplotypes_"
suffix2 = "_ST2A.txt"
#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_diplotypes_19643_ST2A.txt
prefix3 = "hap_diplotypes_"
suffix3 = "_ST2B.txt"

prefix4 = "hap_CYP2D6_"
suffix4 = "_ST2C.txt"
gene2d6 = "CYP2D6"
hap10 = "*10"
# hap0 = "*1/*1"

prefix5 = "hap_SPLIT_"
suffix5 = "_ST2D.txt"

prefix6 = "hap_SPLIT_"
suffix6 = "_ST2E.txt"

prefix7 = "hap_SPLIT_"
suffix7 = "_ST2F.txt"


#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# ===========================================================
fd0 = 2
# ==========================================================
fd1 = 3
fd2 = 5
# ==========================================================
fd3 = 0
fd4 = 32
# ==========================================================


def pgx_hap_step2A(file1, file2):
    # the function select all non-reference diplotypes
    print("Starting Function: pgx_hap_step2A")
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

            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    gene2 = ls2[0]
                    hap_ls = []

                    with open(path_in, "r") as p1:
                        for ln1 in p1:
                            ls1 = ln1.strip().split(s)
                            gene1 = ls1[3]
                            hap1 = ls1[5]
                            hap0 = "*1/*1"

                            if gene2 == gene1 and hap1 != hap0:
                                # print(gene2, hap1, sep=s)
                                hap_ls.append(hap1)

                    if len(hap_ls) == 0:
                        continue
                    else:
                        print(gene2, sc.join(hap_ls), sep=s, file=fileout)

        fileout.close()


def pgx_hap_split_step2B(file1):
    print("Starting Function: pgx_hap_split_step2B")
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix2 + pgx_idx + suffix2
            path_out = dir_path + prefix3 + pgx_idx + suffix3
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    gene1 = ls1[0]
                    dip1B = ls1[1]
                    print(dip1B)

                    if sc in dip1B:
                        dip1_split = dip1B.strip().split(sc)
                        for item in dip1_split:
                            print(gene1, dip1B, item, sep=s, file=fileout)

                    if sc not in dip1B:
                        print(gene1, dip1B, dip1B, sep=s, file=fileout)

        fileout.close()


def pgx_hap_cyp2d6_step2C(file1):
    print("Starting Function: pgx_hap_cyp2d6_step2C")
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            exon9 = int(lsx[17])
            intron2 = int(lsx[18])
            path_in = dir_path + prefix3 + pgx_idx + suffix3  # suffix => _ST2B.txt
            path_out = dir_path + prefix4 + pgx_idx + suffix4  # suffix =>_ST2C.txt
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    gene1 = ls1[0]
                    dip1 = ls1[2]
                    hap1 = dip1.split("/")
                    
                    if gene1 != "CYP2D6":
                        print(s.join(ls1), dip1, sep=s, file=fileout)

                    elif gene1 == "CYP2D6":
                        if exon9 >= 2 and exon9 == intron2:
                            print(s.join(ls1), dip1, sep=s, file=fileout)
                            
                        elif exon9 == 0 and intron2 == 0:
                            print(s.join(ls1), "*5/*5", sep=s, file=fileout)
                        
                        elif exon9 == 1 and intron2 == 1:
                            if hap1.count("*10") == 0:
                                if hap1[0] == "*1" and hap1[1] == "*1":
                                    print(s.join(ls1), "*1/*5", sep=s, file=fileout)
                                elif hap1[0] == "*1" and hap1[1] != "*1":
                                    print(s.join(ls1), hap1[1] + "/*5", sep=s, file=fileout)
                                elif hap1[0] != "*1" and hap1[1] == "*1":
                                    print(s.join(ls1), hap1[0] + "/*5", sep=s, file=fileout)
                                else:
                                    print(s.join(ls1), hap1[0] + "/*5", sep=s, file=fileout)
                            else:
                                print(s.join(ls1), "*5/*36", sep=s, file=fileout)
                        
                        elif exon9 == 1 and intron2 >= 2:
                            if hap1.count("*10") == 0:
                                print(s.join(ls1), "*1/*36", sep=s, file=fileout)
                            else:
                                print(s.join(ls1), "*10/*36", sep=s, file=fileout)

                        elif exon9 == 0 and intron2 >= 2:
                            if hap1.count("*10") == 0:
                                print(s.join(ls1), "*36/*36", sep=s, file=fileout)
                            else:
                                print(s.join(ls1), "*10/*36", sep=s, file=fileout)

                        elif exon9 >= 2 and intron2 >= 2:
                            if exon9 != intron2:
                                division = intron2 / exon9
                                floor = intron2 // exon9
                                n = division % 2
    
                                if division > 1 and n == 0:
                                    times = str(floor)
                                    print(s.join(ls1), "(" + ls1[2] + ")X" + times, sep=s, file=fileout)

                                elif division > 1 and n != 0:
                                    times = str(floor)
                                    print(s.join(ls1), "(" + ls1[2] + ")X" + times, sep=s, file=fileout)
                                
                                else:
                                    print(s.join(ls1), dip1, sep=s, file=fileout)
                        else:
                            print(s.join(ls1), dip1, sep=s, file=fileout)
                    else:
                        print(s.join(ls1), dip1, sep=s, file=fileout)

    fileout.close()


def pgx_dip_clear_step2D(file1):
    print("Starting Function: pgx_dip_clear_step2D")
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix4 + pgx_idx + suffix4  # suffix => _ST2C.txt
            path_out = dir_path + prefix5 + pgx_idx + suffix5  # suffix => _ST2D.txt
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    dip1 = ls1[3].split("/")
                    hap1 = dip1[0]
                    hap2 = dip1[1]
                    print(hap1, hap2, sep=s)

                    if ")" in hap2:
                        x1 = hap1.index("(")
                        y1 = hap2.index(")")
                        allele1 = hap1[x1+1:]
                        allele2 = hap2[:y1]
                        gt1 = allele1 + sf + allele2
                        print(s.join(ls1), gt1, sep=s, file=fileout)
                        print(allele1, allele2, sep=s)

                    if ")" not in hap2 and "X" in hap2:
                        if "X" in hap1:
                            x2 = hap1.index("X")
                            y2 = hap2.index("X")
                            allele1 = hap1[:x2]
                            allele2 = hap2[:y2]
                            gt2 = allele1 + sf + allele2
                            print(s.join(ls1), gt2, sep=s, file=fileout)

                        if "X" not in hap1:
                            # x2 = hap1.index("X")
                            y3 = hap2.index("X")
                            # allele1 = hap1[:x2]
                            allele2 = hap2[:y3]
                            gt3 = hap1 + sf + allele2
                            print(s.join(ls1), gt3, sep=s, file=fileout)

                    if ")" not in hap2 and "X" in hap1:
                        if "X" not in hap2:
                            x4 = hap1.index("X")
                            # y4 = hap2.index("X")
                            allele1 = hap1[:x4]
                            # allele2 = hap2[:y4]
                            gt4 = allele1 + sf + hap2
                            print(s.join(ls1), gt4, sep=s, file=fileout)

                    if ")" not in hap2 and "X" not in hap1:
                        gt5 = hap1 + sf + hap2
                        print(s.join(ls1), gt5, sep=s, file=fileout)

        fileout.close()


def pgx_dip2hap_step2E(file1):
    fnc_name = "Starting Function: pgx_dip2hap_step2E"
    print(fnc_name)
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix5 + pgx_idx + suffix5  # suffix => _ST2D.txt
            path_out = dir_path + prefix6 + pgx_idx + suffix6  # suffix => _ST2E.txt
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    gene = ls1[0]
                    dip1 = ls1[4].split(sf)
                    allele1 = dip1[0]
                    allele2 = dip1[1]
                    gt1 = "*1"

                    if allele1 == allele2 and allele1 == gt1:
                        hap = gene + gt1
                        score = 0
                        print(s.join(ls1), hap, score, sep=s, file=fileout)

                    if allele1 == allele2 and allele2 != gt1:
                        hap = gene + allele2
                        score = 2
                        print(s.join(ls1), hap, score, sep=s, file=fileout)

                    if allele1 != allele2:
                        hap = gene + allele2
                        score = 1
                        print(s.join(ls1), hap, score, sep=s, file=fileout)

    fileout.close()


pgx_hap_step2A(pathx, path2)
time.sleep(5)

pgx_hap_split_step2B(pathx)
time.sleep(5)

pgx_hap_cyp2d6_step2C(pathx)
time.sleep(5)

pgx_dip_clear_step2D(pathx)
time.sleep(10)

pgx_dip2hap_step2E(pathx)
