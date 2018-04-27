# COMP383 Project Repository
# Overview:
A Genome Wide Association Study (GWAS) is a tool used to analyze whether certain variants are associated with a specific trait of interest. Prior to performing the association tests, quality control procedures must be implemented in order to ensure accurate, reproducible, and unbiased results. GWAS often uses linear regression to determine associations, and this requires the use of unrelated individuals. Therefore, related individuals in the GWAS data can pose a problem by confounding the results of the study. Currently, the PLINK software provides bioinformaticians a way to conduct quality control checks on the initial GWAS data before it can be used in the study. Through the use of Python, we developed an automated pipeline that incorporated the major quality control relationship check PLINK commands that need to be performed on the GWAS data, as well as corresponding R plots. This program will allow related individuals to be identified using the PLINK software and visualized from the IBD plots. Individual threshold values for filtering and the choice of viewing plots will be left to user discretion.

# Software Requirements:
Python
R
PLINK
