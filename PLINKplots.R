##MISSING CALL RATE HISTOGRAMS
#read in variant based missing data report file
lmiss <- read.table("man_report.lmiss", header=TRUE)
#histogram of missing call rate
hist(lmiss$F_MISS)
#read in sample based missing data report
imiss <- read.table("manual_report.geno.01.imiss", header =TRUE)
#histogram of missing call rates
hist(imiss$F_MISS)
#read in file after removing missing call rates <99%
postlmiss <- read.table("manual_report.geno.01.lmiss", header = TRUE)
#histrogram of new missing call rate after removal
hist(postlmiss$F_MISS)
#number of SNPs before filtering = 657366
dim(lmiss)[1]
#number of SNPs after filtering = 540524
dim(postlmiss)[1]
#number of indivduals after filtering = 2081
dim(imiss)[1]

##HWE STATS
#read in HWE exact test statistic report
hwe <- read.table("manual_report.geno.01.hwe", header = TRUE)
#summary HWE exact test P-values
summary(hwe$P)
#histogram of hwe P-values
hist(hwe$P)
#find number of SNPs with a P-value of less than 1e-06 = 718 SNPs
table(hwe$P<1e-06)
#find the percentage of SNPs with a P-value less than 1e-06 = .13%
table(hwe$P<1e-06)/sum(table(hwe$P<1e-06))
