
import os


list=[
    # '2017_08_19','2017_09_15','2017_09_25',
# '2017-10-18','2017-11-17','2017-07-12',
# '2017-07-22','2017-08-04','2017-08-11',
# '2017-08-14','2017-08-24','2017-09-10',
# '2017-09-13','2017-09-20','2017-09-23',
# '2018_10_15'
]

# path= "/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/"
path = "/media/vladimir/500STORAGE/SENTINEL/downloads/"
dirs = os.listdir( path )
second_dir = ["ula","ulb"]
i=0
# This would print all the files and directories
for file in dirs:

   if file.find('SAFE')>0: # or zip
    new_date=file[11:19]

    # file_path_ula = '/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/'+new_date[0:4]+"_"+new_date[4:6]+"_"+new_date[6:8]+'/'+second_dir[0]+'/'
    # file_path_ulb = '/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/'+new_date[0:4]+"_"+new_date[4:6]+"_"+new_date[6:8]+'/'+second_dir[1]+'/'
    file_path_ula = '/media/vladimir/500STORAGE/SENTINEL/intermediate/'+new_date[0:4]+"_"+new_date[4:6]+"_"+new_date[6:8]+'/'+second_dir[0]+'/'
    file_path_ulb = '/media/vladimir/500STORAGE/SENTINEL/intermediate/'+new_date[0:4]+"_"+new_date[4:6]+"_"+new_date[6:8]+'/'+second_dir[1]+'/'
    try:
        directory1 = os.path.dirname(file_path_ula)
        os.makedirs(directory1)
        directory2 = os.path.dirname(file_path_ulb)
        os.makedirs(directory2)
        i += 1
    except (OSError):
        print ("folder "+new_date[0:4]+"_"+new_date[4:6]+"_"+new_date[6:8]+" already exist")
        i+=1
print (i)