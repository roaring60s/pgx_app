import time
import statistics
import sys

pathx = sys.argv[1]
dir_path = sys.argv[2]

# pathx = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/biodata/R2_biodata_master.txt"
# dir_path = "/home/p/mygenics/01_system.development/01_PGX/01_mgrc/patients/02A_24/"

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

#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_SRT_GTab0_19637_ST8.txt

# =======================================================
#  /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_combined_19C_SRT_GTab0_19627_ST8.txt

prefix1 = "combined_19C_SRT_GTab0_"
suffix1 = "_ST8.txt"

prefix2 = "hap_drug_list_DD_"
suffix2 = "_ST9.txt"

# /home/p/mygenics/01_system.development/01_PGX/01_mgrc/asa_7C_hap_drug_list_DD_19643_ST9.txt

prefix3 = "combined_preSCORED_"
suffix3 = "_ST10.txt"


prefix4 = "combined_SCORED_"
suffix4 = "_ST11.txt"

#  ========================================================
s = "\t"
sp = "*"
sc = ","
sf = "/"
# ===========================================================

drug_list = []


def fnc_drug_list_step9(file1, pref1, pref2, suf1, suf2):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            pr1 = pref1
            pr2 = pref2
            su1 = suf1
            su2 = suf2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr2 + pgx_idx + su2
            fileout = open(path_out, "w+")
            drug_list.clear()

            with open(path_in, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(s)
                    drug = ls2[14]
                    drug_list.append(drug)

                druglist = list(set(drug_list))
                for item in druglist:
                    print(counter, pgx_idx, sep=s)
                    print(item, file=fileout)
                fileout.close()


def fnc_foldrows_scoring_step10(file1, pref1, pref2, pref3, suf1, suf2, suf3):
    with open(file1, "r")as px:
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            pr1 = pref1
            pr2 = pref2
            pr3 = pref3
            su1 = suf1
            su2 = suf2
            su3 = suf3
            path_in1 = dir_path + pr1 + pgx_idx + su1
            path_in2 = dir_path + pr2 + pgx_idx + su2
            path_out = dir_path + pr3 + pgx_idx + su3
            fileout = open(path_out, "w+")
            drugC_list = []
            brand_list = []
            atc_drug_list = []
            atc_cl1_list = []
            atc_nl1_list = []
            atc_cl3_list = []
            atc_nl3_list = []
            gene_list = []
            idx_list = []
            gtscore_list = []
            ev_list = []
            tier_list = []
            score_list = []
            pheno_list = []
            drugS_list = []
            idtext_list = []
            allele_list = []
            text_list = []
            function_list = []

            with open(path_in2, "r") as p2:
                for ln2 in p2:
                    ls2 = ln2.strip().split(sc)
                    drugx = ls2[0]

                    with open(path_in1, "r") as p1:
                        drugC_list.clear()
                        brand_list.clear()
                        atc_drug_list.clear()
                        atc_cl1_list.clear()
                        atc_nl1_list.clear()
                        atc_cl3_list.clear()
                        atc_nl3_list.clear()
                        gene_list.clear()
                        idx_list.clear()
                        score_list.clear()
                        gtscore_list.clear()
                        ev_list.clear()
                        tier_list.clear()
                        pheno_list.clear()
                        drugS_list.clear()
                        idtext_list.clear()
                        allele_list.clear()
                        text_list.clear()
                        function_list.clear()

                        for ln1 in p1:
                            ls1 = ln1.strip().split(s)
                            pheno = ls1[13].replace("Metabolism/PK", "Efficacy")
                            drugC = ls1[0]
                            brand = ls1[1]
                            atc_drug = ls1[2]
                            atc_cl1 = ls1[3]
                            atc_nl1 = ls1[4]
                            atc_cl3 = ls1[5]
                            atc_nl3 = ls1[6]
                            gene = ls1[7]
                            idx = ls1[8]
                            gtscore = int(ls1[9])
                            ev = ls1[10]
                            tier = ls1[11]
                            idtext = ls1[15]
                            allele = ls1[16]
                            text = ls1[17]
                            function = ls1[18]
                            drugS = ls1[14]
                            score2 = ls1[12]

                            if drugx == drugS:
                                score_list.append(str(score2))
                                drugC_list.append(drugC)
                                brand_list.append(brand)
                                atc_drug_list.append(atc_drug)
                                atc_cl1_list.append(atc_cl1)
                                atc_nl1_list.append(atc_nl1)
                                atc_cl3_list.append(atc_cl3)
                                atc_nl3_list.append(atc_nl3)
                                gene_list.append(gene)
                                idx_list.append(idx)
                                gtscore_list.append(str(gtscore))
                                ev_list.append(ev)
                                tier_list.append(tier)
                                pheno_list.append(pheno)
                                drugS_list.append(drugS)
                                idtext_list.append(idtext)
                                allele_list.append(allele)
                                text_list.append(text)
                                function_list.append(function)

                    list1 = list(set(drugC_list))
                    list2 = list(set(brand_list))
                    list3 = list(set(atc_drug_list))
                    list4 = list(set(atc_cl1_list))
                    list5 = list(set(atc_nl1_list))
                    list6 = list(set(atc_cl3_list))
                    list7 = list(set(atc_nl3_list))
                    list8 = list(set(gene_list))
                    list9 = list(set(idx_list))
                    # list10 = list(set(ev_list))
                    # list11 = list(set(tier_list))
                    list12 = list(set(pheno_list))
                    # list13 = list(set(drugS_list))
                    # list14 = list(set(idtext_list))
                    # list15 = list(set(allele_list))
                    # list16 = list(set(text_list))
                    # list17 = list(set(function_list))

                    print(sc.join(list1), sc.join(list2), sc.join(list3), sc.join(list4), sc.join(list5),
                          sc.join(list6), sc.join(list7), sc.join(list8), sc.join(list9), sc.join(gtscore_list),
                          sc.join(ev_list), sc.join(tier_list), sc.join(score_list), sc.join(list12), drugx, sep=s,
                          file=fileout)

                    print(counter, pgx_idx, drugx, gtscore_list, score_list, sep=s)

            fileout.close()


def fnc_drug_scoring_step11(file1, pref1, pref2, suf1, suf2):
    with (open(file1, "r")as px):
        counter = 0
        for lnx in px:
            counter = counter + 1
            lsx = lnx.strip().split(s)
            pgx_idx = lsx[2]
            pr1 = pref1
            pr2 = pref2
            su1 = suf1
            su2 = suf2
            path_in = dir_path + pr1 + pgx_idx + su1
            path_out = dir_path + pr2 + pgx_idx + su2
            fileout = open(path_out, "w+")
            print(counter, pgx_idx, sep=s)

            with open(path_in, "r") as p1:
                for ln1 in p1:
                    ls1 = ln1.strip().split(s)
                    # gene_ls = ls1[7].split(sc)
                    gt = ls1[9].split(sc)
                    gt_ls = [int(x) for x in gt]
                    ev_ls = ls1[10].split(sc)
                    # tier_ls = ls1[11].split(sc)
                    score = ls1[12].split(sc)
                    score_ls = [round(float(item), 2) for item in score]
                    # pheno_ls = ls1[13].split(sc)

                    res_ls = [gt_ls[i] * score_ls[i] for i in range(len(gt_ls))]
                    # score_average = statistics.mean(res_ls)
                    score_average = sum(res_ls) / len(res_ls)

                    if score_average >= 225:
                        if "1A" in ev_ls or "2A" in ev_ls or "1B" in ev_ls:
                            # if "Tier 1 VIP" in tier_ls:
                            weight3 = 3
                            print(s.join(ls1), weight3, sep=s, file=fileout)

                    if score_average >= 225:
                        if "1A" not in ev_ls and "2A" not in ev_ls and "1B" not in ev_ls:
                            # if "Tier 1 VIP" in tier_ls:
                            weight2 = 2
                            print(s.join(ls1), weight2, sep=s, file=fileout)

                    if 15 < score_average < 225:
                        weight2a = 2
                        print(s.join(ls1), weight2a, sep=s, file=fileout)

                    if 0 < score_average <= 15:
                        weight1 = 1
                        print(s.join(ls1), weight1, sep=s, file=fileout)

                fileout.close()


fnc_drug_list_step9(pathx, prefix1, prefix2, suffix1, suffix2)
time.sleep(10)


fnc_foldrows_scoring_step10(pathx, prefix1, prefix2, prefix3, suffix1, suffix2, suffix3)
time.sleep(10)


fnc_drug_scoring_step11(pathx, prefix3, prefix4, suffix3, suffix4)
