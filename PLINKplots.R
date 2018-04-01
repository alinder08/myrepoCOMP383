##MISSING CALL RATE HISTOGRAMS

#variant based missing data report file

lmiss <- read.table("man_report.lmiss", header=TRUE)

#histogram of missing call rate

hist(lmiss$F_MISS)

#sample based missing data report

imiss <- read.table("manual_report.geno.01.imiss", header =TRUE)

#histogram of missing call rates

hist(imiss$F_MISS)

#file after removing missing call rates <99%

postlmiss <- read.table("manual_report.geno.01.lmiss", header = TRUE)

#histrogram of new missing call rate after removal

hist(postlmiss$F_MISS)
