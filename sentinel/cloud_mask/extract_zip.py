import zipfile
import os



i=0
j=0
#path = "/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/"
path = "/media/vladimir/500STORAGE/SENTINEL/downloads/"
dirs = os.listdir( path )

# This would print all the files and directories
for file in dirs:
   i += 1
   if file.find('zip')>0:
       j+=1
       fantasy_zip = zipfile.ZipFile(path+file)
       fantasy_zip.extractall(path)
       fantasy_zip.close()

print ('all documents: ',i)
print ('zip: ',j)

