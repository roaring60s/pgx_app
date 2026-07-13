#! /bin/bash

# The script processes Results in ASA format and generate Pharmacogenetics Report.
# Scoring can be amended in STEP 9, function => "fnc_pgx_ST9_10_11_scoring_090225.py"

# Date run: 19/06/2026

# Sample details:
# MG2600013/
# /media/D1/patients/B000_mygenics/MG2600013/pgx_exome_hap_MG2600013_ST1A.txt
# /media/D1/patients/B000_mygenics/MG2600013/pgx_exome_var_MG2600013
# /media/D1/patients/B000_mygenics/MG2600013/biodata/MG2600013_biodata_master.txt

#Anatomical Therapeutic Chemical (ATC) Classification

# *********************  Variables That Are Manually Changed For Each Run *********************************************

# date1 variable shows current date
date1=$(date +'%d.%m.%y')
pgx_code="PGX01"

dir="/media/D1/patients/B000_nara/"
# name is used for on-screen messages only
name="MG2600972"
batch="MG2600972"
# run is used in naming files
run="MG2600972"

report1="25_06_2026"
report2="25/06/2026"

batchd="$dir/$batch/"

# *********************  Non-Changeable Variables  ********************************************************************

biodatad=$batchd"biodata"
#datad="$batchd/data_pgx"
final_dir=$batchd"final"

bio_path=$biodatad/$run'_biodata_master.txt'
dir_path="$batchd/pgx_exome_"

# Python interpreter (pinned to avoid relying on PATH resolution / mixed versions)
pythonbin="/usr/bin/python3.10"

# Python directory
pythond="/home/p/mygenics/app_pgx/python/"

# Annotation reference directory
annd="/home/p/mygenics/app_pgx/ann/"

#-----------------------------------------------------------------------------------------------------------------------
# shellcheck disable=SC2034
hap_snps_master="$annd/pgx_asa_hap_snps_master_05.01.2024.txt"

hap_alleles_master="$annd/pgx_asa_hap_alleles_master_090225.txt"

variants_snps_master="$annd/pgx_asa_variants_snps_master_05.01.2024.txt"

hap_genes_1C="$annd/pgx_hap_genes_1C_SRT_DD_UX.txt"

var_clin_alleles_EV13="$annd/pgx_asa_var_clin_alleles_EV13_160325.txt"

hap_clin_alleles_EV13="$annd/pgx_asa_hap_clin_alleles_EV13_160325.txt"

drugs_ann_cln_ann_EV13="$annd/drugs_cln_anno_160325.txt"

atcl5_dx_table_ev_ab4="$annd/pgx_asa_atc5_druglist_evab4_4C_160325.txt"

atc_1level="$annd/atc_1level_codes.txt"

brand_names="$annd/pgx_all_drugs_brand_master_atc1_160325.txt"

echo ""
echo ""
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   PIPELINE   PROCESSING  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
echo ""
echo "===================================  STEP 0-A  DEMOGRAPHIC FILES ================================================"
echo ""
echo "                   Generating samples demographic data for the report for $name @: $(date)"
echo ""
#
time "$pythonbin" "$pythond/fnc_pgx_sample_bio_data_23.03.24.py" "$bio_path" "$batchd/" "$report1" "$report2"
wait

echo ""
echo '========================================  HAP STEP 1-B  ========================================================'
echo ""
echo "Step 1-B: HAP => Haplotypes Generation for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_hap_alleles_1B_020425.py" "$bio_path" "$hap_alleles_master" "$dir_path"
wait

echo ""
echo '======================================= HAP STEPS 2A, 2B, 2C, 2D ==============================================='
echo ""
echo "Steps 2A, 2B, 2C: HAP => Assign Diplotypes for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_hap_assign_diplotypes_ST2A2B2C_070925.py" "$bio_path" "$hap_genes_1C" "$dir_path"
wait

echo ""
echo '======================================  VAR Step 3 => Annotating with Clinical Alleles  ========================'
echo ""
echo "Step 3: VAR => Annotating with Clinical Alleles for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_var_clin_ST3_02.02.24.py" "$bio_path" "$var_clin_alleles_EV13" "$dir_path"
wait

echo ""
echo '======================================  HAP STEP 3 => Annotating with Clinical Alleles ========================='
echo ""
echo "Step 3: HAP => Annotating with Clinical Alleles for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_hap_clin_ST3_03.02.24.py" "$bio_path" "$hap_clin_alleles_EV13" "$dir_path"
wait

echo ""
echo '===================================== VAR STEP => Annotating with Drugs ======================================='
echo ""
echo "Step 4: VAR => Annotating with Drugs for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_var_dx_ST4_02.02.24.py" "$bio_path" "$drugs_ann_cln_ann_EV13" "$dir_path"
wait

echo ""
echo '===================================== HAP STEP 4 => Annotating with Drugs ======================================'
echo ""
echo "Step 6: HAP => Annotating with Drugs for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_hap_dx_ST4_03.02.24.py" "$bio_path" "$drugs_ann_cln_ann_EV13" "$dir_path"
wait

echo ""
echo '==================================== STEPS 5, 6: HAP and VAR => Combining ======================================'
echo ""
echo "Step 5 and 6: HAP and VAR => Combining Haplotypes and Variant Files for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_combining_hap_var_ST5.6_03.02.24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '=================================== STEPS 7 ,8: Sorting with PANDAS ============================================'
echo ""
echo "Step 7 and 8: COMBINED => Pandas, Sorting for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_pandas_SRT_ST7.8_03.02.24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '========================================= STEPS 9, 10, 11: Generating Scoring =================================='
echo ""
echo ""
echo "Step 9, 10, 11: Generating Scoring for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_ST91011_scoring_200925.py" "$bio_path" "$dir_path"
wait

echo ""
echo '========================================= STEPS 12, 13, 14: Generating Table 1   ==============================='
echo ""
echo "Step 12, 13, 14: Generating Table 1 for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_table1_28_12_24.py" "$bio_path" "$atcl5_dx_table_ev_ab4" "$atc_1level" "$dir_path"
wait

echo ""
echo '======================================  STEP 16, 17: Generating Gene Table  ===================================='
echo ""
echo "Step 16: Generating Gene Input Table for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_gene_table_step16_04.02.24.py" "$bio_path" "$dir_path"
wait
echo ""
echo "----------------------------------------------------------------------------------------------------------------"
echo ""
echo "Step 17: Generating Final Gene Table for $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/pgx_gene_table_final_11_12_24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '=============================  STEP 18, Table 3: Generating Interim File  ======================================='
echo "                                          $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_table3_step18_07.02.24.py" "$bio_path" "$dir_path"

wait
echo ""
echo '======================  STEP 19 & 20, Table 3: Adding Brand Name & Formatting Comma  ============================'
echo "                                         $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_table3_brand_step19_03_12_24.py"  "$bio_path" "$brand_names" "$dir_path"

wait
echo ""
echo '======================  STEP 21, Table 3: Final Formatting: Replacing Comma with New Line ======================='
echo "                                         $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_table3_replace_comma_28_12_24.py" "$bio_path" "$dir_path"

echo ""
echo '===============================  STEP 22, Table 2: Generating Input File ======================================='
echo "                                            $name @: $(date)"
echo ""

echo "Generating Table2 Input File "

time "$pythonbin" "$pythond/fnc_pgx_table2_fInput_24_12_24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '===============================  STEP 23, Table 2: Generating Final File ======================================='
echo "                                            $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/fnc_pgx_table2_step23_05_12_24.py" "$bio_path" "$dir_path"

echo ""
echo '===============================  STEP 24, Natural-Sorting Gene Table HAP Column ======================================='
echo "                                            $name @: $(date)"
echo ""

time "$pythonbin" "$pythond/gene_sorting_01.py" "$bio_path" "$dir_path"
wait

echo ""
echo '===============================  STEP 25, Copying Final Files ======================================='
echo "                                            $name @: $(date)"
echo ""

cp "$batchd"*final* "$final_dir"
echo ""
echo '================================================================================================================'
echo ""
echo "------*****************   END OF PGX PIPELINE for $name @: $(date)  ********************------------------------"
echo ""
echo ""
echo '================================================================================================================'
