"""
Call a program using subprocess
"""
import os           #so we can change the eviroment of the subprocesses
import subprocess   #so we can call a subprocess

def callShellCmd_Sample():
    """
    """
    cr = call("dir>fred.txt", shell=True)
    print("Done")


def getSexCheckProblems(inSexCheck, outSexCheckProblems, outSexCheckRemovals):
    """
    Examine the rows of the inFile for the search term "Problem" and return the number of rows found with that term
    write the problem rows to a .sexcheck-problems file
    wirte the problem id;s to a .sexcheck-removals file
    """
    #open the output files
    oProblems = open(outSexCheckProblems, 'w')
    oRemovals = open(outSexCheckRemovals, 'w')

    problemsFound = 0
    #open the input file
    ifile = open(inSexCheck, 'r')
    for line in ifile:
        if line.find("PROBLEM") > -1:   #if the line has a problem send it to the output files
            problemsFound += 1
            oProblems.write(line)
            fields=line.split()
            oRemovals.write(fields[0] + " " + fields[1] +"\n")
    oProblems.close
    oRemovals.close
    return problemsFound

def Task_CheckSex(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to do a Sex Check

    Step01 Check if there are any Problems by running
        exePath + 'plink.exe --bfile ' + inPath + dsName + ' --check-sex --out ' + outPath + dsName +'-Step01'
    if datasetStep01 has problems:
        try to fix the problems
        plink ....
        if datasetStep02 has problems:
            remove offending data
    retrun the datasetName
    """
    #Step01
    stepId = "S01"      #Step 01
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    plinkCmd = " --check-sex "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId
    cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
    print(cmd)
    subprocess.Popen(cmd, cwd = pyScriptPath)

    #See if there were any problems found in Step01
    inSexCheck = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck"
    outSexCheckProblems = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck-problems"
    outSexCheckRemovals = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck-removals"
    cnt1 = getSexCheckProblems(inSexCheck, outSexCheckProblems, outSexCheckRemovals)

    if cnt1 > 0:
        #Step02 Try to correct check-sex problems from the raw datafile
        inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
        plinkCmd = " --impute-sex --make-bed "
        stepId = "S02"
        outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId
        cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
        subprocess.Popen(cmd, cwd = pyScriptPath)

        #See if there were any problems found in Step02 that were not fixed
        inSexCheck = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck"
        outSexCheckProblems = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck-problems"
        outSexCheckRemovals = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId + ".sexcheck-removals"
        cnt2 = getSexCheckProblems(inSexCheck, outSexCheckProblems, outSexCheckRemovals)
        if cnt2 > 0:
            #remove the bad data
            inDataSetName = outDataSetName
            plinkCmd = " --remove " + outSexCheckRemovals + " --make-bed "
            stepId = "S03"
            outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + taskId + stepId
            cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
            subprocess.Popen(cmd, cwd = pyScriptPath)
    #return the dataset produced by this task
    return(os.path.join(dataPath, inDsName, outDir), inDsName + "-" + taskId + stepId)


def Task01_CheckSex(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to do a Sex Check

    """
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    plinkCmd = " --check-sex --missing "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)


def Task02_Geno(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to Recalculate individual call rates after removing SNPs with call rates <99%  

    """
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    plinkCmd = " --geno 0.01 --make-bed "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)
#

    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --missing "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)


def Task03_HWE(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to Calculate HWE statistics to flag SNPs later

    """
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --hardy "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)


def Task04_Prune(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to LD prune (rm 1 SNP if r2>0.3 in 50 SNP window) for relationship check and heterozygosity calculation

    """
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --indep-pairwise 50 5 0.3 "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)


def Task05_Relationship(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to perform a Relationship check

    """
    program = os.path.join(exePath, "plink.exe")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    extractDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01.prune.in"
    plinkCmd = " --genome --min 0.05 "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01.rc"
    cmd = program + " --bfile " + inDataSetName + " --extract " + extractDataSetName + plinkCmd + "--out " + outDataSetName
    print(cmd)
    subprocess.call(cmd, cwd = pyScriptPath)


#main
cwd = os.getcwd()
pyScriptPath = os.path.dirname(os.path.abspath(__file__))   # where the python pipeline lives
if cwd != pyScriptPath:
    print("Run the pipeline script from the directory where the script is located")
    print("All paths are reletive to that one")
    exit

exePath = r"..\programs"
dataPath = r"..\data"
inDir = r"1Raw"
inDsName = "dataset1"
outDir = "3Wip"
print("start")
Task01_CheckSex("T01", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
Task02_Geno("T02", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
Task03_HWE("T03", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
Task04_Prune("T04", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
Task05_Relationship("T05", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
print("Done")
