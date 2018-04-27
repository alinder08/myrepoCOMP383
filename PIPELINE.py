"""
Python Pipeline to ....

The pipline returns exit codes, 
0 is success
negative codes are from the pipline
    -1 pipline not started in the correct directory
    -2 invalid pipeline command line such as a bad parameter
positive error codes are from plink. This is from plink and each error code has a specific meaning 

"""
import argparse     #for command line processing
import os           #so we can change the enviroment of the subprocesses
import subprocess   #so we can call a subprocess

def Task01_CheckSex(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to do a Sex Check
    """
    program = os.path.join(exePath, "plink")
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    plinkCmd = " --check-sex --missing "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName

    print("\n>>>>> Task01_ChckSex plink command is")
    print(">>>>>" + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4 usage
    exitCode = subprocess.call(cmd, shell=True) #Python 3.5.2 usage 
    return(exitCode)


def Task02_Geno(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir, geno="0.01"):
    """
    Use Plink to Recalculate individual call rates after removing SNPs with call rates <99%  
    """
    program = os.path.join(exePath, "plink")
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    plinkCmd = " --geno " + geno + " --make-bed "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print("\n>>>>> Task02_Geno_Step01 plink command is")
    print(">>>>> " + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True) #3.5.2
#
    if(exitCode !=0):
        return(exitCode)

    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --missing "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + " --out " + outDataSetName
    print("\n>>>>> Task02_Geno_Step02 plink command is")
    print(">>>>> " + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True)#3.5.2
    return(exitCode)


def Task03_HWE(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to Calculate HWE statistics to flag SNPs later
    """
    program = os.path.join(exePath, "plink")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --hardy "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print("\n>>>>> Task03_HWE plink command is")
    print(">>>>> " + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True) #3.5.2
    return(exitCode)

def Task04_Prune(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    Use Plink to LD prune (rm 1 SNP if r2>0.3 in 50 SNP window) for relationship check and heterozygosity calculation
    """
    program = os.path.join(exePath, "plink")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    plinkCmd = " --indep-pairwise 50 5 0.3 "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    cmd = program + " --bfile " + inDataSetName + plinkCmd + "--out " + outDataSetName
    print("\n>>>>> Task04_Prune plink command is")
    print(">>>>> " + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True) #3.5.2
    return(exitCode)

def Task05_Relationship(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir, fFilter):
    """
    Use Plink to perform a Relationship check
    """
    program = os.path.join(exePath, "plink")
    inDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01"
    extractDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01.prune.in"
    plinkCmd = " --genome --min 0.05 "
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report.geno.01.rc"
    cmd = program + " --bfile " + inDataSetName + " --extract " + extractDataSetName + plinkCmd + "--out " + outDataSetName
    print("\n>>>>> Task05_Relationship plink command is")
    print(">>>>> " + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True) #3.5.2
    # 
    if(fFilter > 0):
        totalRows, removedRows = relationshipFilter(outDataSetName + ".genome", outDataSetName + ".Cleaned", outDataSetName + ".Removed", fFilter)
        print("Total rows in genome file = ", totalRows)
        print("Rows removed with filter of {0} = {1}".format(fFilter, removedRows))
    return(exitCode)

def relationshipFilter(inputFile, outCleaned, outRemoved, fFilter):
    """
    Examine the rows of the inputFile for the PI_HAT values ???? and filter them from the output
    write the good rows to the clean file
    wirte the problem rows to the removed file
    """
    #open the output files
    oCleaned = open(outCleaned, 'w') #this is a "clean" .genome file with removals removed
    oRemoved = open(outRemoved, 'w') #this is a file of the removed individuals

    problemsFound = 0
    rows = 0
    #open the input file
    ifile = open(inputFile, 'r')
    for line in ifile:
        if (rows == 0):     #write the header to both outputs
            oCleaned.write(line)
            oRemoved.write(line)
        else:
            fields=line.split()
            PI_HAT = float(fields[9])
            if (PI_HAT <= fFilter):   #if the line has os ok send it to the output files
                oCleaned.write(line)
            else:
                problemsFound += 1 #The number of people removed who do not satisfy the pi-hat vals
                oRemoved.write(line)
        rows += 1 #Total number of people in the original genome file

    oCleaned.close
    oRemoved.close
    return (rows -1, problemsFound) # remove one for the header


def Task06_MakePlots(taskId, pyScriptPath, exePath, dataPath, inDir, inDsName, outDir):
    """
    USE R to make plots of the information from each dataset
    """
    program = exePath
    inDataSetName = os.path.join(dataPath, inDsName, inDir, inDsName)
    rCmd = " PIPELINE_Scripts.r"
    outDataSetName = os.path.join(dataPath, inDsName, outDir, inDsName) + "-" + "report"
    cmd = program + rCmd + " " + inDataSetName + " " + outDataSetName

    print("\n>>>>> Task06_MakePlots r command is")
    print(">>>>>" + cmd + "\n")
    #exitCode = subprocess.call(cmd, cwd = pyScriptPath) #3.6.4
    exitCode = subprocess.call(cmd, shell=True) #3.5.2
    return(exitCode)


def main():
    # make sure the pipline is being run from the correct directory
    cwd = os.getcwd().lower()
    pyScriptPath = os.path.dirname(os.path.abspath(__file__)).lower()   # where the python pipeline lives
    if cwd != pyScriptPath:
        print("Run the pipeline script from the directory where the script is located")
        print("All paths used are reletive to that one")
        print("The Pipeline assumes this directory structure\n")
        print(r"../Data/<DataSetName>")
        print(r"../Data/<DataSetName>/1Raw")
        print(r"../Data/<DataSetName>/2Manual")
        print(r"../Data/<DataSetName>/3Wip")
        print(r"../Data/<DataSetName>/4Output")
        print(r"../programs (where plink is installed)")
        print(r"../src (where this program is)")
        exit(-1) #This is to make sure that you run the program from the proper directory 

    # get the datasetname and optional parameters from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", help="Name of the dataSet, this is required ")
    parser.add_argument("--Geno", type=float, help="Geno parameter default = 0.01")
    parser.add_argument("--Filter", type=float, help="Filter relationships with phat > entered value.  Default is no filter")
    parser.add_argument("--ContinueOnError", action="store_true", help="Continue processing tasks when a task generates an error default = False")
    args = parser.parse_args() #The above allow the user to pick plink parameters from the command line. Defaults are set.
    print("Pipeline running with the following parameters: ")
    print("Dataset: ")
    print(args.dataset)
    print("Geno: ")
    print(args.Geno)
    print("Filtering: ")
    print(args.Filter)

    #if args.Geno is None set to default
    #Else check that it is between ? and ?
    if (args.Geno == None): 
        sGeno = ".01"
    elif not (args.Geno > .001 and args.Geno < .0999 ):
        print("Geno must be greater than .001 and less than .0999")
        exit(-2)
    else:
        sGeno = str(args.Geno) #save value

    #if args.Filter is None set to default
    #Else check that it is between ? and ?
    if (args.Filter == None):
        fFilter = 0.0
    elif not (args.Filter > .01 and args.Filter < .9 ):
        print("Filter must be greater than .01 and less than .9")
        exit(-2)
    else:
        fFilter = args.Filter

    #main if you wish to change the directory structure or names from the provided default, do so using the variables below.
    #exePath = r"../programs"    #Windows
    exePath = r""    #linux
    dataPath = r"../data"
    inDir = r"1Raw"
    inDsName = args.dataset
    outDir = "3Wip"
    print("Starting pipeline")
    
    exitCode = Task01_CheckSex("T01", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
    if(args.ContinueOnError == False and exitCode != 0):
        print("\nPipelineError: Task01_CheckSex returned an error from plink.  The value was " + str(exitCode) )
        exit(exitCode)
    exitCode = Task02_Geno("T02", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir, sGeno)
    if(args.ContinueOnError == False and exitCode != 0):
        print("\nPipelineError: Task02_Geno returned an error from plink.  The value was " + str(exitCode) )
        exit(exitCode)
    exitCode = Task03_HWE("T03", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
    if(args.ContinueOnError == False and exitCode != 0):
        print("\nPipelineError: Task03_HWE returned an error from plink.  The value was " + str(exitCode) )
        exit(exitCode)
    exitCode = Task04_Prune("T04", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
    if(args.ContinueOnError == False and exitCode != 0):
        print("\nPipelineError: Task04_Prune returned an error from plink.  The value was " + str(exitCode) )
        exit(exitCode)
    exitCode = Task05_Relationship("T05", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir, fFilter)
    if(args.ContinueOnError == False and exitCode != 0):
        print("\nPipelineError: Task05_Relationship returned an error from plink.  The value was " + str(exitCode) )
        exit(exitCode)
        
#if you need to configure your R locations, do so here.        
    #exePath = r'"C:/Program Files/R/R-3.4.4/bin/Rscript.exe"'   #windows
    exePath = r'"Rscript"'  #linux    
    dataPath = r"../data"
    inDir = r"3Wip"
    inDsName = args.dataset
    outDir = "4Output"
    exitCode = Task06_MakePlots("T06", pyScriptPath, exePath, dataPath, inDir, inDsName, outDir)
    print("Pipeline Completed Succesfuly")
    

if __name__ == '__main__': #run like a program without having an ide open. 
    main()

