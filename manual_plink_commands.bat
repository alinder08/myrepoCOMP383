rem T01_CheckSex.bat
rem This batch file is to consistently run plink with specific command line options

..\..\programs\plink.exe --bfile ..\..\data\dataset1\1Raw\dataset1 --check-sex --out ..\..\data\dataset1\2Manual\T01A\dataset1

..\..\programs\plink.exe --bfile ..\..\data\dataset1\1Raw\dataset1 --impute-sex --make-bed --out ..\..\data\dataset1\2Manual\T01B\dataset1

..\..\programs\plink.exe --bfile ..\..\data\dataset1\2Manual\T01B\dataset1 --check-sex --out ..\..\data\dataset1\2Manual\T01B\dataset9
