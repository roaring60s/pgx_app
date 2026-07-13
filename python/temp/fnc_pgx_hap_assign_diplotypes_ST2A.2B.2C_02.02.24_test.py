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
hap0 = "*1/*1"

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


def pgx_hap_step2A(file1, file2, no0, no1, no2, no3):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[no0]
            path_in = dir_path + prefix1 + pgx_idx + suffix1
            path_out = dir_path + prefix2 + pgx_idx + suffix2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(file2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    gene2 = ls2[no3]
                    hap_ls = []

                    with open(path_in, "r") as p1:
                        for ln1 in p1:
                            ls1 = ln1.strip().split(s)
                            gene1 = ls1[no1]
                            hap1 = ls1[no2]

                            if gene2 == gene1 and hap1 != hap0:
                                # print(gene2, hap1, sep=s)
                                hap_ls.append(hap1)

                        if len(hap_ls) == 0:
                            hap_ls.append(hap0)
                            print(gene2, sc.join(hap_ls), sep=s, file=fileout)
                        else:
                            print(gene2, sc.join(hap_ls), sep=s, file=fileout)

        fileout.close()


def pgx_hap_split_step2B(file1):
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
                    dip1 = ls1[1]
                    print(dip1)

                    if sc in dip1:
                        dip1_split = dip1.strip().split(sc)
                        for item in dip1_split:
                            print(gene1, dip1, item, sep=s, file=fileout)

                    if sc not in dip1:
                        print(gene1, dip1, dip1, sep=s, file=fileout)

        fileout.close()


def pgx_hap_cyp2d6_step2C(file1):
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

                    if gene1 != gene2d6:
                        print(s.join(ls1), dip1, sep=s, file=fileout)

                    if gene1 == gene2d6:
                        if exon9 == 2 and exon9 == intron2:
                            print(s.join(ls1), dip1, sep=s, file=fileout)
                        if exon9 == 2 and intron2 < 2:
                            print(s.join(ls1), dip1, sep=s, file=fileout)

                        if exon9 == 1 and intron2 == 1:
                            hap1 = dip1.split("/")

                            if hap1[0] == "*1" and hap1[1] == "*1":
                                print(s.join(ls1), "*1/*5", sep=s, file=fileout)
                            if hap1[0] == "*1" and hap1[1] != "*1":
                                print(s.join(ls1), hap1[1] + "/*5", sep=s, file=fileout)
                            if hap1[0] != "*1" and hap1[1] == "*1":
                                print(s.join(ls1), hap1[0] + "/*5", sep=s, file=fileout)
                            if hap1[0] != "*1" and hap1[1] != "*1":
                                print(s.join(ls1), hap1[0] + "/*5", sep=s, file=fileout)

                        if exon9 != intron2 and intron2 > 2:
                            division = intron2 / exon9
                            n = division % 2

                            if n == 0:
                                hap1 = dip1.split("/")
                                times = str(intron2 - exon9)

                                if hap1.count(hap10) == 2:
                                    assigned_dip2 = "(*10/*36)X" + times
                                    print(s.join(ls1), assigned_dip2, sep=s, file=fileout)

                                if hap1.count(hap10) == 0:
                                    assigned_dip0 = "(dip1)X" + times
                                    print(s.join(ls1), assigned_dip0, sep=s, file=fileout)

                                if hap1.count(hap10) == 1:
                                    assigned_dip1 = "(*1/*36)X" + times
                                    print(s.join(ls1), assigned_dip1, sep=s, file=fileout)

                            if n != 0:
                                hap1 = dip1.split(sf)
                                times = str(intron2 - exon9)

                                if hap1.count(hap10) == 2:
                                    assigned_dip02 = hap10 + "X" + str(exon9) + "/" + "*36X" + times
                                    print(s.join(ls1), assigned_dip02, sep=s, file=fileout)

                                if hap1.count(hap10) == 0:
                                    assigned_dip00 = "(" + dip1 + ")" + "X" + times
                                    print(s.join(ls1), assigned_dip00, sep=s, file=fileout)

                                # if hap1.count(hap10) == 1 and hap1[0] == hap10:
                                #     assigned_dip010 = hap1[1] + "X" + str(exon9) + "/" + hap1[0] + "X" + times
                                #     print(s.join(ls1), assigned_dip010, sep=s, file=fileout)

                                if hap1.count(hap10) == 1 and hap1[1] == hap10:
                                    assigned_dip01 = hap1[0] + "X" + str(exon9) + "/" + hap1[1] + "X" + times
                                    print(s.join(ls1), assigned_dip01, sep=s, file=fileout)

    fileout.close()


def pgx_dip_clear_step2D(file1):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split("\t")
            pgx_idx = lsx[2]
            path_in = dir_path + prefix4 + pgx_idx + suffix4  # suffix => _ST2C.txt
            path_out = dir_path + prefix5 + pgx_idx + suffix5  # suffix => _ST2D.txt
            fileout = open(path_out, "w+")

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    dip1 = ls1[3]
                    print(counter, pgx_idx, sep=s)

                    if ")X" in dip1:
                        x = dip1[1:-3]
                        print(s.join(ls1), x, sep=s, file=fileout)

                    if ")X" not in dip1 and "X" in dip1:
                        dip1_split = dip1.split(sf)
                        al1 = dip1_split[0]
                        al2 = dip1_split[1]
                        x = al1.index("X")
                        y = al2.index("X")
                        allele1 = al1[:x]
                        allele2 = al2[:y]
                        diplotype = allele1 + sf + allele2
                        print(s.join(ls1), diplotype, sep=s, file=fileout)

                    else:
                        print(s.join(ls1), dip1, sep=s, file=fileout)

        fileout.close()


def pgx_dip2hap_step2E(file1):
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


pgx_hap_step2A(pathx, path2, fd0, fd1, fd2, fd3)
time.sleep(5)

pgx_hap_split_step2B(pathx)
time.sleep(5)

pgx_hap_cyp2d6_step2C(pathx)
time.sleep(5)

pgx_dip_clear_step2D(pathx)
time.sleep(5)

pgx_dip2hap_step2E(pathx)
