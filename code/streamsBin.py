from osgeo import gdal
from os import listdir,path,walk
import sys,math,time,numpy
from numba import jit
@jit(nopython=True,nogil=True)
def toBin(inArray,newArray,noDataVal):
    # newArray.astype(int)
    # print inArray.shape,"yaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaay"
    for i in range(0,len(inArray)):
        for j in range(0,len(inArray[i])):
            if int(inArray[i][j]) != int(noDataVal):
                newArray[i][j] = 1
    return newArray
if __name__=="__main__":
    # streamsFile=r"C:\Users\Bharath\Documents\TWRIS\tankCatchment\streamSegements.tif"
    streamsFile=sys.argv[1]
    print "processing",streamsFile
    streamsRaster=gdal.Open(streamsFile)
    noDataVal=int(streamsRaster.GetRasterBand(1).GetNoDataValue())

    inArray=streamsRaster.ReadAsArray()
    # inArray=inArray.astype(int32)
    outArray=numpy.zeros((inArray.shape))
    # outArray=outArray.astype(int32)
    # print inArray.dtype,inArray.shape,noDataVal,outArray.dtype,outArray.shape

    outArray=toBin(inArray,outArray,noDataVal)

    # print outArray
    # sys.exit()

    driver = gdal.GetDriverByName('HFA')
    outRaster = driver.Create(streamsFile[:-4]+"bin.img", streamsRaster.RasterXSize, streamsRaster.RasterYSize, 1, gdal.GDT_Byte, ['NBITS=1'])
    outRaster.SetGeoTransform(streamsRaster.GetGeoTransform())
    outband = outRaster.GetRasterBand(1)
    outRaster.SetProjection(streamsRaster.GetProjection())
    outband.WriteArray(outArray)
    outband.FlushCache()
    outRaster.FlushCache()
