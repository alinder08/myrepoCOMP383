# COMP383 Project Repository
# Overview:
A Genome Wide Association Study (GWAS) is a tool used to analyze whether certain variants are associated with a specific trait of interest. Prior to performing the association tests, quality control procedures must be implemented in order to ensure accurate, reproducible, and unbiased results. GWAS often uses linear regression to determine associations, and this requires the use of unrelated individuals. Therefore, related individuals in the GWAS data can pose a problem by confounding the results of the study. Currently, the PLINK software provides bioinformaticians a way to conduct quality control checks on the initial GWAS data before it can be used in the study. Through the use of Python, we developed an automated pipeline that incorporated the major quality control relationship check PLINK commands that need to be performed on the GWAS data, as well as corresponding R plots. This program will allow related individuals to be identified using the PLINK software and visualized from the IBD plots. Individual threshold values for filtering and the choice of viewing plots will be left to user discretion.

# Software Requirements:
Python

R

PLINK

# Input Files

.bim/.bed/.fam files

# Output Files

After Step 1: .sexcheck

After Step 2: .imiss/.lmiss

After Step 3: .hwe

After Step 4:.pune.in /.prune.out

After Step 5: .genome

# Functions

The PPRA is broken up into 6 functions which are:
1.       Task01_CheckSex
2.       Task02_Geno
3.       Task03_HWE
4.       Task04_Prune
5.       Task05_Relationship
6.       Task06_MakePlots

Task01_CheckSex runs the following PLINK command:
..\programs\plink.exe --bfile ..\data\dataset1\1Raw\dataset1 --check-sex --missing  --out ..\data\dataset1\3Wip\dataset1-report

Task02_Geno runs the following PLINK commands:
..\programs\plink.exe --bfile ..\data\dataset1\1Raw\dataset1 --geno .01 --make-bed --out ..\data\dataset1\3Wip\dataset1-report.geno.01
..\programs\plink.exe --bfile ..\data\dataset1\3Wip\dataset1-report.geno.01 --missing  --out ..\data\dataset1\3Wip\dataset1-report.geno.01

Task03_HWE runs the following PLINK command:
..\programs\plink.exe --bfile ..\data\dataset1\3Wip\dataset1-report.geno.01 --hardy --out ..\data\dataset1\3Wip\dataset1-report.geno.01

Task04_Prune runs the following command:
..\programs\plink.exe --bfile ..\data\dataset1\3Wip\dataset1-report.geno.01 --indep-pairwise 50 5 0.3 --out ..\data\dataset1\3Wip\dataset1-report.geno.01

Task05_Relationship runs the following command:
..\programs\plink.exe --bfile ..\data\dataset1\3Wip\dataset1-report.geno.01 --extract ..\data\dataset1\3Wip\dataset1-report.geno.01.prune.in --genome --min 0.05 --out ..\data\dataset1\3Wip\dataset1-report.geno.01.rc

Task06_MakePlots invokes the PIPELINE_Scripts.r. This file, which can be edited by the user, can be used to generate any desired plots for the analysis of the dataset. The provided R scripts produce the following plots:

1.       A histogram of lmiss$F_MISS

The .lmiss file that was created after the variant missing call rate command was conducted was used to create a histogram of the F_MISS values in R. The number of SNPs present in the file before filtering was also calculated.

2.       A histogram of imiss$F_MISS

Similar to the .lmiss file, the .imiss file that was created after the sample missing call rate command was then input into R to create a histogram of the F_MISS values. The number of individuals present after filtering was also counted.

3.       A histogram of postImiss$F_MISS

After the missing call rates under 99% were removed, the new .lmiss file was read into R. A histogram of the new F_MISS values was then made, and the number of SNPs present after the filtering was also calculated.

4.       A histogram of hwe$P

The .hwe file was the output of the hardy weinberg check command in PLINK and contained the exact hardy weinberg test statistics. The p-values from this file were used to plot a histogram. The number of percentage of SNPs that contained a p-value under 1e-06 was generated.

5.       An unfiltered IBD plot of the dataset
6.       An accompanying histogram of pi-hat of the unfiltered IBD plot

After the relationship check PLINK command, the newly generated .genome file was input in R in order to create an ibd plot based on the Z0 and Z1 scores. The Z0 score represents the probability that the IBD is 0, whereas the Z1 score represents the probability that the IBD is 1. Related individuals can be visualized based on their location on the IBD plot. A histogram was also created using the PI_HAT (proportion of IBD) values.

7.       A filtered IBD plot of the dataset (if the filter step has been chosen by the user)
8.       An accompanying histogram of PIi-HAT of the filtered IBD plot (if filter step has been chosen by the user)

