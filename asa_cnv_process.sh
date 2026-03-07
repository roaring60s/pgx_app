#! /bin/bash

dir="/media/p/D11/patients/2025/MGRC_20250725/"
final="/media/p/D11/patients/2025/MGRC_20250725/final/"
sample="21592"
sample_id="21592"
asa_dir="/media/p/D11/patients/2025/MGRC_20250725/data_pgx/2025723_209005460013_V0_Hg37_NONCLUSTER.txt"

exon9="/home/p/mygenics/prj_pgx/asa_cnv/CYP2D6_exon9_rsID.txt"
intron2="/home/p/mygenics/prj_pgx/asa_cnv/CYP2D6_intron2_rsID.txt"
g6pd="/media/p/D11/patients/B013_20240807/biodata/G6PD_rsids.txt"

echo "Processing CYP2D6 Exon 9 Variants"
grep -f $exon9 $asa_dir | grep $sample_id > $final$sample'_exone9_rsid.txt'

echo "Processing CYP2D6 Intron 2 Variants"
grep -f $intron2 $asa_dir | grep $sample_id > $final$sample'_intron2_rsid.txt'

echo "Processing G6PD Variants"
grep -f $g6pd $asa_dir | grep $sample_id > $final$sample'_G6PD_rsid.txt'
