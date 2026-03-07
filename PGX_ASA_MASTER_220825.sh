#! /bin/bash

# The script processes Results in ASA format and generate Pharmacogenetics Report.
# Scoring can be amended in STEP 9, function => "fnc_pgx_ST9_10_11_scoring_090225.py"
# Anatomical Therapeutic Chemical (ATC) Classification

# RUN 15-01-2026: MGRC
# /media/D1/patients/2026/MGRC_20260114/biodata/MGRC_20260114_biodata_master.txt
# //media/D1/patients/2026/MGRC_20260114/data_pgx/20260114_209971290001_V0_Hg37_CLUSTER.txt

# *********************  Variables That Are Manually Changed For Each Run *********************************************

# date1 variable shows current date
date1=$(date +'%d.%m.%y')
pgx_code="PGX03"

name="MGRC_20260114"  # => change e.g MGRC_batch, after 2024
run="MGRC_20260114"  # => change e.g MGRC_batch, after 2024

report1="16_01_2026"  # => change
report2="16/01/2026"  # => change

dir="/media/D1/patients/2026/"  # => change to the current year path e.g. /2025, after 2024
batch="MGRC_20260114"  # => change e.g MGRC_batch, after 2024
batchd="$dir/$batch/"  # => change
asa_run="20260114_209971290001"  # => change
asa1="20260114_209971290001_V0_Hg37_CLUSTER.txt"  # => change
asa2="asa_$asa_run.txt"
#asa_suffix="_V0_CLUSTER.txt"

lab="MGRC"  # second option if "AGTC" => if option, uncomment line below
#lab="AGTC"  # second option is "MGRC" => if option, uncomment line above

# *********************  Non-Changeable Variables  ********************************************************************

biodatad="$batchd/biodata/"
datad="$batchd/data_pgx"
final_dir="$batchd/final"

asa_in="$datad/$asa1"
#asa_out1="$batchd/$asa2.tsv"
asa_out="$batchd/$asa2"

bio_path=$biodatad$batch'_biodata_master.txt'  # => change
dir_path="$batchd/asa_"

# Python directory
pythond="/home/p/mygenics/prj_pgx/python"

#-----------------------------------------------------------------------------------------------------------------------

# shellcheck disable=SC2034
hap_snps_master="./ann/pgx_asa_hap_snps_master_05.01.2024.txt"

hap_alleles_master="./ann/pgx_asa_hap_alleles_master_090225.txt"

variants_snps_master="./ann/pgx_asa_variants_snps_master_05.01.2024.txt"

hap_genes_1C="./ann/pgx_hap_genes_1C_SRT_DD_UX.txt"

var_clin_alleles_EV13="./ann/pgx_asa_var_clin_alleles_EV13_160325.txt"

hap_clin_alleles_EV13="./ann/pgx_asa_hap_clin_alleles_EV13_200925.txt"

drugs_ann_cln_ann_EV13="./ann/drugs_cln_anno_160325.txt"

atcl5_dx_table_ev_ab4="./ann/pgx_asa_atc5_druglist_evab4_4C_160325.txt"

atc_1level="./ann/atc_1level_codes.txt"

brand_names="./ann/pgx_all_drugs_brand_master_atc1_160325.txt"

echo ""
echo ""
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>   PIPELINE   PROCESSING  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
echo ""
echo "===================================  STEP 0-A  DEMOGRAPHIC FILES ================================================"
echo ""
echo "                   Generating samples demographic data for the report for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_sample_bio_data_23.03.24.py" "$bio_path" "$batchd/" "$report1" "$report2"

echo ""
echo "=====================================  STEP 0-B  TRIMMING ASA FILE =============================================="
echo ""
echo "Step 0-B: Generating 7 Columns ASA file from ASA for $name @: $(date)"
echo ""

#----------------------------------------------------------------------------------------------------------------------
#	For MGRC the range is sed '1,9d'
#	For AGTC the range is sed '1,11d'
#	From ASA are extracted:
#	Col  1 = SNP Name
#	Col  2 = Sample ID
#	Col  5 = GC Score
#	Col 23 = SNP
#	Col 27 = Plus/Minus Strand
#	Col 17 = Allele1 - Plus
#	Col 18 = Allele2 - Plus

#----------------------------------------------------------------------------------------------------------------------
#Check the value of the lab variable and execute the corresponding sed command
#For "SED" command, do not use "-i" option. It means in place.

if [[ "$lab" == "AGTC" ]]; then
  sed '1,11d' "$asa_in" | awk '{FS=OFS="\t"} {print $1,$2,$5,$23,$27,$17,$18}' > $asa_out  # Delete the first 11 lines if lab is AGTC, then extract 7 columns
elif [[ "$lab" == "MGRC" ]]; then
  sed '1,10d' "$asa_in" | awk '{FS=OFS="\t"} {print $1,$2,$5,$23,$27,$17,$18}' > $asa_out  # Delete the first 9 lines if lab is MGRC,, extract 7 columns
else
  echo "Invalid lab value."  # Handle cases where the lab value is neither MGRC nor AGTC
fi
wait

echo ""
echo '=====================================  STEP 0-C  Generating ASA sample files ===================================='
echo ""
echo "Step 0-C: Generating ASA sample files from ASA 7 Columns file for $name @: $(date)"
echo ""

time python "$pythond/fnc_PGX_ST0C_select_samples_from_ASA_260625.py" "$bio_path" "$asa_out" "$dir_path"
wait

echo ""
echo '======================================  HAP STEP 1-A  =========================================================='
echo ""
echo "Step 1-A: HAP => Selection HAP SNPs for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_select_snps4haps_step1A_12_12_24.py" "$bio_path" "$hap_snps_master" "$dir_path"
wait

echo ""
echo '========================================  HAP STEP 1-B  ========================================================'
echo ""
echo "Step 1-B: HAP => Haplotypes Generation for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_hap_allels_1B_12_12_24.py" "$bio_path" "$hap_alleles_master" "$dir_path"
wait

echo ""
echo '=======================================  VAR STEP 1 Variants annotation ========================================'
echo ""
echo "Step 1: VAR => Variants annotation for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_select_snps4variants_step1_12_12_24.py" "$bio_path" "$variants_snps_master" "$dir_path"
wait

echo ""
echo '======================================= HAP STEPS 2A, 2B, 2C, 2D ==============================================='
echo ""
echo "Steps 2A, 2B, 2C: HAP => Assign Diplotypes for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_hap_assign_diplotypes_ST2A2B2C_070925.py" "$bio_path" "$hap_genes_1C" "$dir_path"
wait

echo ""
echo '======================================  VAR Step 3 => Annotating with Clinical Alleles  ========================'
echo ""
echo "Step 3: VAR => Annotating with Clinical Alleles for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_var_clin_ST3_02.02.24.py" "$bio_path" "$var_clin_alleles_EV13" "$dir_path"
wait

echo ""
echo '======================================  HAP STEP 3 => Annotating with Clinical Alleles ========================='
echo ""
echo "Step 3: HAP => Annotating with Clinical Alleles for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_hap_clin_ST3_220825.py" "$bio_path" "$hap_clin_alleles_EV13" "$dir_path"
wait

echo ""
echo '===================================== VAR STEP => Annotating with Drugs ======================================='
echo ""
echo "Step 4: VAR => Annotating with Drugs for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_var_dx_ST4_02.02.24.py" "$bio_path" "$drugs_ann_cln_ann_EV13" "$dir_path"
wait

echo ""
echo '===================================== HAP STEP 4 => Annotating with Drugs ======================================'
echo ""
echo "Step 6: HAP => Annotating with Drugs for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_hap_dx_ST4_03.02.24.py" "$bio_path" "$drugs_ann_cln_ann_EV13" "$dir_path"
wait

echo ""
echo '==================================== STEPS 5, 6: HAP and VAR => Combining ======================================'
echo ""
echo "Step 5 and 6: HAP and VAR => Combining Haplotypes and Variant Files for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_combining_hap_var_ST5.6_03.02.24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '=================================== STEPS 7 ,8: Sorting with PANDAS ============================================'
echo ""
echo "Step 7 and 8: COMBINED => Pandas, Sorting for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_pandas_SRT_ST7.8_03.02.24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '========================================= STEPS 9, 10, 11: Generating Scoring =================================='
echo ""
echo ""
echo "Step 9, 10, 11: Generating Scoring for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_ST91011_scoring_200925.py" "$bio_path" "$dir_path"
wait

echo ""
echo '========================================= STEPS 12, 13, 14: Generating Table 1   ==============================='
echo ""
echo "Step 12, 13, 14: Generating Table 1 for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_table1_28_12_24.py" "$bio_path" "$atcl5_dx_table_ev_ab4" "$atc_1level" "$dir_path"
wait

echo ""
echo '======================================  STEP 16, 17: Generating Gene Table  ===================================='
echo ""
echo "Step 16: Generating Gene Input Table for $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_gene_table_step16_04.02.24.py" "$bio_path" "$dir_path"
wait
echo ""
echo "----------------------------------------------------------------------------------------------------------------"
echo ""
echo "Step 17: Generating Final Gene Table for $name @: $(date)"
echo ""

time python "$pythond/pgx_gene_table_final_11_12_24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '=============================  STEP 18, Table 3: Generating Interim File  ======================================='
echo "                                          $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_table3_step18_07.02.24.py" "$bio_path" "$dir_path"

wait
echo ""
echo '======================  STEP 19 & 20, Table 3: Adding Brand Name & Formatting Comma  ============================'
echo "                                         $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_table3_brand_step19_03_12_24.py"  "$bio_path" "$brand_names" "$dir_path"

wait
echo ""
echo '======================  STEP 21, Table 3: Final Formatting: Replacing Comma with New Line ======================='
echo "                                         $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_table3_replace_comma_28_12_24.py" "$bio_path" "$dir_path"

echo ""
echo '===============================  STEP 22, Table 2: Generating Input File ======================================='
echo "                                            $name @: $(date)"
echo ""

echo "Generating Table2 Input File "

time python "$pythond/fnc_pgx_table2_fInput_24_12_24.py" "$bio_path" "$dir_path"
wait

echo ""
echo '===============================  STEP 23, Table 2: Generating Final File ======================================='
echo "                                            $name @: $(date)"
echo ""

time python "$pythond/fnc_pgx_table2_step23_05_12_24.py" "$bio_path" "$dir_path"

echo ""
echo '===============================  STEP 24, Copying Final Files ======================================='
echo "                                            $name @: $(date)"
echo ""

cp -fuv "$batchd"*final* "$final_dir"
echo ""
echo '================================================================================================================'
echo ""
echo "------*****************   END OF PGX PIPELINE for $name @: $(date)  ********************------------------------"
echo ""
echo ""
echo '================================================================================================================'
