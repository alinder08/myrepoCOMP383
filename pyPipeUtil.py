"""
pyPipeUtil
    pyPipeUtil --MakeDatasetDir <DataSet>
        create ..\Data\<DataSet>
        create ..\Data\<DataSet>\1Raw
        create ..\Data\<DataSet>\2Manual
        create ..\Data\<DataSet>\3Wip
        create ..\Data\<DataSet>\4Output
    pyPipeUtil --Clean <DataSet>
        delete ..\Data\<DataSet>\3Wip\*.*
        delete ..\Data\<DataSet>\4Output\*.*

"""
import argparse
import os

def MakeDatasetDir (dataSet):
    baseDir = os.path.join("..","Data",dataSet)
    os.mkdir(baseDir)
    os.mkdir(os.path.join(baseDir,"1Raw"))
    os.mkdir(os.path.join(baseDir,"2Manual"))
    os.mkdir(os.path.join(baseDir,"3Wip"))
    os.mkdir(os.path.join(baseDir,"4Output"))


def Clean (dataSet):
    baseDir = os.path.join("..","Data",dataSet)
    myfile = os.path.join(baseDir,"3Wip")
    DeleteAllFilesInFolder(myfile)
    myfile = os.path.join(baseDir,"4Output")
    DeleteAllFilesInFolder(myfile)


def DeleteAllFilesInFolder(folder):
    for fileName in os.listdir(folder):
        file_path = os.path.join(folder, fileName)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def main():
    # get the command and the datasetname from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--MakeDatasetDir", action="store_true", help="Make a Dataset directory")
    parser.add_argument("--Clean", action="store_true", help="Clean the Dataset")
    parser.add_argument("dataSet", help="Name of the dataSet")
    args = parser.parse_args()
    print(args.MakeDatasetDir, args.dataSet)

    if args.MakeDatasetDir == True:
        MakeDatasetDir(args.dataSet)
    if args.Clean == True:
        Clean(args.dataSet)

if __name__ == '__main__':
    main()

