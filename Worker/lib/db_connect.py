import os
#Rough

folderpath="../Input/sources/vid1"
if len(os.listdir(folderpath)) == 0:
    print("Directory is empty")
else:
    print("Directory is not empty")
files=os.listdir(folderpath)
#print(files)
for filename in files :
    print(filename)
    if filename.split('.')[-1]=='mp4':
        xfname=os.path.join(folderpath,filename.split('.')[0]+'.xml')
        print(xfname)
        if os.path.exists(xfname)==True:
            print("done")

