"""
This script changes the names of many files, e.g. single excitation spectrum
files.
___
Input:
Create a .txt file where you copy all the wavelenght/ filename extensions
like:
573
573.2
573.25
...
Put the .txt and all the files which filenames need to be changed in the
same folder.
The script will ask you to do so.
Then it will ask for the file stem.
___
Output:
New files with the stem you defined and the wavelenghts added like:
outputstem_xxxxx.asc
in new folder named: renamed

Old files will be moved to ..\\archive\\<file stem>\\

Date: 30/07/2018
Last update: 04/03/2019
Creator: Manuel Eibl
"""
import os
import sys
import shutil
import HumanSorting as hs

#set path to directory where the files are
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

newpath = str(path + '\\renamed')
if os.path.exists(newpath):
    shutil.rmtree(newpath)

StartingCondition1 = ("Plese copy your files which you want to rename in the folder: \n" + str(path) +"\n")
StartingCondition2 = ("Please change the excitation wavelengths in the file ExcitationWavelengths.txt \nto fit yours;\nuse format xxx.xx or xxx.x or xxx\n")
print(StartingCondition1)
print(StartingCondition2)

input("Press Enter when ready...")


#changes current directory to the path
#load wavelenght data
FNAME = "ExcitationWavelengths.txt" #Change to your .txt file!
#open data and write in list called data
temp = open(FNAME, "r")
data = [x.replace("\n","") for x in temp.readlines()]
temp.close()

#modify data to xxx.xx shape
for (n, item) in enumerate(data):
    if len(data[n]) == 5:
        #data[n] = data[n] + '0'
        data[n] += '0'
    if len(data[n]) == 3:
        data[n] += '00'
    data[n] = data[n].replace(".", "")
    data[n] = data[n].replace(",","")

#list of old filenames
dirListing = os.listdir(path)
OLDNAMES = []
text = input("What is your file stem? (e.g. ABC1 for ABC1_1, ABC1_2...)")  #Change to your file stem!

filestem = (str(text))

for item in dirListing:
    if filestem in item:
        OLDNAMES.append(item)

#sorts the list in the order 1,2,3,... instead of 1,10,100,11,...
hs.sort_nicely(OLDNAMES)
#creates new sub folder if it doesn't exist, change folder if you want to

if not os.path.exists(newpath):
    os.makedirs(newpath)
#copies the files into sub folder
for file_name in OLDNAMES:
    full_file_name = os.path.join(path, file_name)
    if (os.path.isfile(full_file_name)):
        shutil.copy(full_file_name, './renamed')

os.chdir(newpath)

i = 0
for item in OLDNAMES:
    os.rename(OLDNAMES[i], str(filestem) + '_' + data[i] +".asc")   #Change!
    # Change to your preferred output file stem
    i = i+1

os.chdir(path)

path_archive = str(path + '\\archive')
if not os.path.exists(path_archive):
    os.makedirs(path_archive)


os.chdir(path_archive)

subpath_archive = str(path_archive + '\\' + str(filestem))
if not os.path.exists(subpath_archive):
    os.makedirs(subpath_archive)

os.chdir(path)
i = 0
for item in OLDNAMES:
    shutil.move(os.path.join(path, OLDNAMES[i]), os.path.join(subpath_archive, OLDNAMES[i]))
    i = i+1
