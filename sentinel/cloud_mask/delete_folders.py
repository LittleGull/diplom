import os,subprocess
i=0
j=0
# path = "/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/"
path = "/media/vladimir/500STORAGE/SENTINEL/downloads/"
dirs = os.listdir( path )
print (dirs)
# list = dirs[81:160] //when use big massiv
list = dirs
print (list)
# This would print all the files and directories
for file in list:
   i += 1
   if file.find('SAFE')>0:
        j+=1
        p = subprocess.Popen('rm -rf '+path+file+'/*', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # p = subprocess.Popen('/opt/sen2cor/Sen2Cor-02.05.05-Linux64/bin/L2A_Process --resolution 20 /media/vladimir/500STORAGE/ETALON/SENTINEL/2018/'+file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p = subprocess.Popen('rmdir '+path+file, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p.stdout.readlines():
            print (line)
        retval = p.wait()
print ('all documents: ',i)
print ('safe: ',j)