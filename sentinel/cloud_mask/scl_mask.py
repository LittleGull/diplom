from osgeo import gdal
import os,subprocess
i=0
# path = "/media/vladimir/500STORAGE/ETALON/SENTINEL/2018/"
path = "/media/vladimir/500STORAGE/SENTINEL/downloads"

dirs = os.listdir( path )
print (dirs)
# list = dirs[81:160] //when use big massiv

for file in dirs:
   i += 1
   if file.find('SAFE')>0:
       if file.find('L2A') > 0:
           data='20181129'
           if file.find(data) > 0:
               print(file)
               a=''.join(next(os.walk(path+'/'+file+'/GRANULE'))[1])
               b = next(os.walk(path + '/' + file + '/GRANULE/'+a+'/IMG_DATA/R20m/'))[2]
               for m in b:
                   if m.find('SCL') > 0:
                    f=path + '/' + file + '/GRANULE/'+a+'/IMG_DATA/R20m/'+m
                    print (f)
                    # os.rename(path + '/' + file + '/GRANULE/'+a+'/IMG_DATA/R20m/'+m, '/media/vladimir/500STORAGE/SENTINEL/downloads/'+m)
                    # filename="S2A_MSIL1C_20180416T081601_N0206_R121_T38ULA_20180416T102454_RGB.tif"

                    fileformat = "GTiff"
                    driver = gdal.GetDriverByName(fileformat)
                    metadata = driver.GetMetadata()
                    if metadata.get(gdal.DCAP_CREATE) == "YES":
                        print("Driver {} supports Create() method.".format(fileformat))

                    if metadata.get(gdal.DCAP_CREATE) == "YES":
                        print("Driver {} supports CreateCopy() method.".format(fileformat))
                    src_ds = gdal.Open(f)
                    dst_ds = driver.CreateCopy('g.tif', src_ds, strict=1, options=["TILED=YES", "COMPRESS=PACKBITS"])
                    # # Once we're done, close properly the dataset
                    gt = dst_ds.GetGeoTransform()
                    gtLst = list(gt)
                    gtLst[1] = 10
                    gtLst[5] = -10
                    gm = dst_ds.RasterXSize


                    gm=10980
                    dst_ds.RasterXSize.insert(gm)
                    print(dst_ds.RasterXSize)
                    # dst_ds.RasterXSize=gm
                    dst_ds.SetGeoTransform(gtLst)
                    print("Size is {} x {} x {}".format(dst_ds.RasterXSize,
                                                        dst_ds.RasterYSize,
                                                        dst_ds.RasterCount))

                    # dst_ds.SetGeoTransform([300000, 10, 0, 409800, 0, -10])   #!!!!!!!!!!

                    dst_ds = None
                    src_ds = None