import os
path='/home/user/vat/VideoAnalyticsPlatform_v7/Inference_copy/Input'
sub_source_paths=[]
for subdir, dirs, files in os.walk(path):
    for file in files:
            print(file)
            sub_source_paths.append(os.path.join(subdir))
sub_source_paths=list(set(sub_source_paths))
print("listttttttttttttt",sub_source_paths)
for foldername in sub_source_paths:
    print(foldername)
    files=os.listdir(foldername)
#files=os.listdir("./Input")
    for filename in files :
                
        print(filename)
        pa=os.path.join(foldername,filename)
        print(pa)

