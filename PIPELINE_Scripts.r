args = commandArgs(trailingOnly=TRUE)
#args[1] is the location of the Wip directory with the base dataset name 
# ie - "..\data\dataset1\3Wip\dataset1"

#args[2] is the location of the Output directory with the base dataset name 
# ie - "..\data\dataset1\4Output\dataset1"

print(args[1])  
print(args[2])

#PLOT TASK02-
fileToPlot = paste(args[1], "-report.lmiss", sep="")##MISSING CALL RATE HISTOGRAMS
plotOutput = paste(args[2], "-Ranalysis.png", sep="") #let's you change the name of the png generated
#read in variant based missing data report file
lmiss <- read.table(fileToPlot, header=TRUE)
pdf(plotOutput)
#histogram of missing call rate
hist(lmiss$F_MISS)
#number of SNPs before filtering = 657366
dim(lmiss)[1]


#plot Task03
#read in sample based missing data report
fileToPlot = paste(args[1], "-report.geno.01.imiss", sep="")
#plotOutput = paste(args[2], "-Ranalysis.pdf", sep="")
imiss <- read.table(fileToPlot, header =TRUE)
#histogram of missing call rates
hist(imiss$F_MISS)
#number of indivduals after filtering = 2081
dim(imiss)[1]

#read in file after removing missing call rates <99%
fileToPlot = paste(args[1], "-report.geno.01.lmiss", sep="")
postlmiss <- read.table(fileToPlot, header = TRUE)
#histrogram of new missing call rate after removal
hist(postlmiss$F_MISS)
#number of SNPs after filtering = 540524
dim(postlmiss)[1]


#plot Task04
#read in HWE exact test statistic report
fileToPlot = paste(args[1], "-report.geno.01.hwe", sep="")
hwe <- read.table(fileToPlot, header = TRUE)
#summary HWE exact test P-values
summary(hwe$P)
#histogram of hwe P-values
hist(hwe$P)
#find number of SNPs with a P-value of less than 1e-06 = 718 SNPs
table(hwe$P<1e-06)
#find the percentage of SNPs with a P-value less than 1e-06 = .13%
table(hwe$P<1e-06)/sum(table(hwe$P<1e-06))


#plot Task05
# concatenate Args[1] with the rest of the datafilename
fileToPlot = paste(args[1], "-report.geno.01.rc.genome", sep="")
library(ggplot2)
#read in genome file for ibd values and plots
ibd <- read.table(fileToPlot, header = TRUE)
#plot fo Z0 vs Z1
qplot(Z0,Z1,data=ibd, colour=RT, xlim=c(0,1), ylim=c(0,1))
#histogram of PI_HAT values
hist(ibd$PI_HAT)
#pull any duplicates
dups <- data.frame()
for(i in 1:dim(ibd)[1]){
  if(as.character(ibd$IID1[i]) == as.character(ibd$IID2[i])){
    dups <- rbind(dups,ibd[i,])
  }
}
#number of duplicates- none found in this sample
dim(dups)

#cleaned .genome if filtering is done
fileToPlot = paste(args[1], "-report.geno.01.rc.Cleaned", sep="")
library(ggplot2)
#read in genome file for ibd values and plots
ibd <- read.table(fileToPlot, header = TRUE)
#plot fo Z0 vs Z1
qplot(Z0,Z1,data=ibd, colour=RT, xlim=c(0,1), ylim=c(0,1))
#histogram of PI_HAT values
hist(ibd$PI_HAT)
#pull any duplicates
dups <- data.frame()
for(i in 1:dim(ibd)[1]){
  if(as.character(ibd$IID1[i]) == as.character(ibd$IID2[i])){
    dups <- rbind(dups,ibd[i,])
  }
}
#number of duplicates- none found in this sample
dim(dups)

print("Plots Completed")