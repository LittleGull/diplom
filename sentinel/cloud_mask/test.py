# # import os, sys
# # import qgis
# # from PyQt5.QtWidgets import QApplication
# #
# # app = QApplication(sys.argv)
# # qgis_prefix = os.getenv("/usr/lib/qgis")
# # qgis.core.QgsApplication.setPrefixPath(qgis_prefix, True)
# # qgis.core.QgsApplication.initQgis()
# # print (1)
# #
# from qgis.core import *
#
# # supply path to qgis install location
# QgsApplication.setPrefixPath("/usr/lib/qgis", True)
#
# # create a reference to the QgsApplication, setting the
# # second argument to False disables the GUI
# qgs = QgsApplication([], False)
#
# # load providers
# qgs.initQgis()
#
# uri="/media/vladimir/500STORAGE/ETALON/SENTINEL/S2A_MSIL1C_20180416T081601_N0206_R121_T38ULA_20180416T102454_RGB.tif"
#
# layer=QgsRasterLayer(uri, "layer name you like", "delimitedtext")
# file_writer=QgsRasterFileWriter(layer)
# pipe = QgsRasterPipe()
#
#
#
#
# file_writer.writeRaster(
#
#     provider.xSize(),
#     provider.ySize(),
#     provider.extent(),
#     provider.crs())
# # a=QgsRasterFileWriter.maxTileHeight(10).maxTileWidth(10).
# # QgsMapLayerRegistry.instance().addMapLayer(layer)
#
# # Write your code here to load some layers, use processing algorithms, etc.
# print (1)
#
# # #uri = "E:/Geodata/qgis_sample_data/raster/SR_50M_alaska_nad.tif"
# #
# # rlayer = iface.addRasterLayer(uri,"my raster","gdal")
# #
# # if rlayer.isValid():
# #     print("This is a valid raster layer!")
# # else:
# #     print("This raster layer is invalid!")
# # When your script is complete, call exitQgis() to remove the provider and
# # layer registries from memory
# qgs.exitQgis()
#
# import struct // not use
import osr
import numpy

from osgeo import gdal
filename="S2A_MSIL1C_20180416T081601_N0206_R121_T38ULA_20180416T102454_RGB.tif"
dataset = gdal.Open(filename, gdal.GA_ReadOnly)
if dataset:
    print("Driver: {}/{}".format(dataset.GetDriver().ShortName,
                                 dataset.GetDriver().LongName))
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                        dataset.RasterYSize,
                                        dataset.RasterCount))
    print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    if geotransform:
        print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    print("_____Fetching a Raster Band_____")
    band = dataset.GetRasterBand(1)
    print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))

    min = band.GetMinimum()
    max = band.GetMaximum()
    if not min or not max:
        (min, max) = band.ComputeRasterMinMax(True)
    print("Min={:.3f}, Max={:.3f}".format(min, max))

    if band.GetOverviewCount() > 0:
        print("Band has {} overviews".format(band.GetOverviewCount()))

    if band.GetRasterColorTable():
        print("Band has a color table with {} entries".format(band.GetRasterColorTable().GetCount()))
    print("____Reading Raster Data______")
    scanline = band.ReadRaster(xoff=0, yoff=0,
                               xsize=band.XSize, ysize=1,
                               buf_xsize=band.XSize, buf_ysize=1,
                               buf_type=gdal.GDT_Float32)

print("____Techniques for Creating Files______")
fileformat = "GTiff"
driver = gdal.GetDriverByName(fileformat)
metadata = driver.GetMetadata()
if metadata.get(gdal.DCAP_CREATE) == "YES":
    print("Driver {} supports Create() method.".format(fileformat))

if metadata.get(gdal.DCAP_CREATE) == "YES":
    print("Driver {} supports CreateCopy() method.".format(fileformat))
print("____Using CreateCopy2()______")
src_ds = gdal.Open(filename)
dst_ds = driver.CreateCopy('2.tiff', src_ds, strict=0,   # 1 значит точно эквивалентно оригиналу
                                   options=["TILED=YES"])  #убрали сжатие
# Once we're done, close properly the dataset
dst_ds = None
# src_ds = None
print("____Using CreateCopy3()______")
src_ds = gdal.Open(filename)
dst_ds = driver.CreateCopy('3.tiff', src_ds, strict=1,  # 1 значит точно эквивалентно оригиналу
                           options=["TILED=YES", "COMPRESS=PACKBITS"])  # убрали сжатие
# Once we're done, close properly the dataset
dst_ds = None
# src_ds = None
#
print("____Using CreateCopy1()______")
src_ds = gdal.Open(filename)
dst_ds = driver.CreateCopy('1.tiff', src_ds, strict=0,  # исходные настройки
                           options=["TILED=YES", "COMPRESS=PACKBITS"])
# Once we're done, close properly the dataset
dst_ds.SetGeoTransform([300000, 10, 0, 5600040, 0, -30])

dst_ds = None
src_ds = None
#
print("____Using CopyFiles()______")
src_ds = gdal.Open(filename)
dst_ds = driver.CreateCopy('copy.tiff', src_ds)
# Once we're done, close properly the dataset
dst_ds = None
src_ds = None
print("____Using Create()______")
dst_ds = driver.Create( 'new.tif', 512, 512, 1, gdal.GDT_Byte )


dst_ds.SetGeoTransform([444720, 30, 0, 3751320, 0, -30])
srs = osr.SpatialReference()
srs.SetUTM(11, 1)
srs.SetWellKnownGeogCS('NAD27')
dst_ds.SetProjection(srs.ExportToWkt())
raster = numpy.zeros((512, 512), dtype=numpy.uint8)
dst_ds.GetRasterBand(1).WriteArray(raster)
# Once we're done, close properly the dataset
dst_ds = None

