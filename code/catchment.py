import gdal
import numpy,numba
from os import listdir,path,walk,system,sys
from math import ceil,floor
import time
from numba import jit
"""
    77.26744369,20.06364357
    Requires above mentioned packages
"""
def readReleventArray(raster,gt,point):
    nB=gt[3]
    sB=gt[3]+gt[5]*raster.RasterYSize+gt[5]
    eB=gt[0]+gt[1]*raster.RasterXSize+gt[1]
    wB=gt[0]
    regionBounds=[point[0]-compBuf,point[1]+compBuf,point[0]+compBuf,point[1]-compBuf]
    if regionBounds[1]<float(nB):
        nB=regionBounds[1]
    if regionBounds[0]>float(wB):
        wB=regionBounds[0]
    if regionBounds[2]<float(eB):
        eB=regionBounds[2]
    if regionBounds[3]>float(sB):
        sB=regionBounds[3]
    arrayBounds=[int((wB-gt[0])/gt[1]),int((nB-gt[3])/gt[5]),int((eB-gt[0])/gt[1]),int((sB-gt[3])/gt[5])]
    pointPixel=[floor((point[0]-gt[0])/gt[1]),floor((point[1]-gt[3])/gt[5])]
    # print arrayBounds[0],arrayBounds[1],arrayBounds[2]-arrayBounds[0],arrayBounds[3]-arrayBounds[1]
    print pointPixel
    releventArray=raster.ReadAsArray(arrayBounds[0],arrayBounds[1],arrayBounds[2]-arrayBounds[0]-1,arrayBounds[3]-arrayBounds[1]-1)
    # print releventArray
    return releventArray,arrayBounds,pointPixel
@jit(nopython=True,nogil=True)
def Core(inArray,point):
    point=[int(point[1]),int(point[0])]
    outArray=numpy.zeros(inArray.shape)
    toChklist=[point]
    iter=0
    while iter<len(toChklist):
    # for eachPoint in toChklist:
        eachPoint=toChklist[iter]
        # if eachPoint!=None:
        #     continue
        # print eachPoint
        # for i in [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
        outArray[int(eachPoint[0]),int(eachPoint[1])]=1
        if inArray[eachPoint[0]+1,eachPoint[1]+1]==3:
            outArray[eachPoint[0]+1,eachPoint[1]+1]=1
            toChklist.append([eachPoint[0]+1,eachPoint[1]+1])
        if inArray[eachPoint[0]+1,eachPoint[1]]==2:
            outArray[eachPoint[0]+1,eachPoint[1]]=1
            toChklist.append([eachPoint[0]+1,eachPoint[1]])
        if inArray[eachPoint[0]+1,eachPoint[1]-1]==1:
            outArray[eachPoint[0]+1,eachPoint[1]-1]=1
            toChklist.append([eachPoint[0]+1,eachPoint[1]-1])
        if inArray[eachPoint[0],eachPoint[1]+1]==4:
            outArray[eachPoint[0],eachPoint[1]+1]=1
            toChklist.append([eachPoint[0],eachPoint[1]+1])
        if inArray[eachPoint[0],eachPoint[1]-1]==8:
            outArray[eachPoint[0],eachPoint[1]-1]=1
            toChklist.append([eachPoint[0],eachPoint[1]-1])
        if inArray[eachPoint[0]-1,eachPoint[1]+1]==5:
            outArray[eachPoint[0]-1,eachPoint[1]+1]=1
            toChklist.append([eachPoint[0]-1,eachPoint[1]+1])
        if inArray[eachPoint[0]-1,eachPoint[1]]==6:
            outArray[eachPoint[0]-1,eachPoint[1]]=1
            toChklist.append([eachPoint[0]-1,eachPoint[1]])
        if inArray[eachPoint[0]-1,eachPoint[1]-1]==7:
            outArray[eachPoint[0]-1,eachPoint[1]-1]=1
            toChklist.append([eachPoint[0]-1,eachPoint[1]-1])
        # print inArray[eachPoint[0]+1,eachPoint[1]+1]
        # print inArray[eachPoint[0]+1,eachPoint[1]]
        # print inArray[eachPoint[0]+1,eachPoint[1]-1]
        # print inArray[eachPoint[0],eachPoint[1]+1]
        # print inArray[eachPoint[0],eachPoint[1]-1]
        # print inArray[eachPoint[0]-1,eachPoint[1]+1]
        # print inArray[eachPoint[0]-1,eachPoint[1]]
        # print inArray[eachPoint[0]-1,eachPoint[1]-1]
        # print len(toChklist)
        # raw_input("Test")
        iter+=1
        # print len(toChklist),toChklist,eachPoint,iter
        # toChklist.remove(eachPoint)
        # toChklist=toChklist[1:]
    return outArray
    # print toChklist
    # while True:
    #     pixelsIn=len(addedList)
    #     for eachPoint in toChklist:
    #         for i in range(0,8):
    #             array[point[1],point[0]]
    #         toChklist.remove(eachPoint)
def getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj):
    arrayTopCords=[gt[0]+arrayBounds[0]*gt[1],gt[3]+arrayBounds[1]*gt[5]]
    pointPixel=[pointPixel[0]-arrayBounds[0],pointPixel[1]-arrayBounds[1]]
    outArray=Core(relArray,pointPixel)
    driver = gdal.GetDriverByName('GTIFF')
    outRaster = driver.Create(outFile, relArray.shape[1],relArray.shape[0], 1, gdal.GDT_Byte, ['NBITS=1'])
    outRaster.SetGeoTransform([arrayTopCords[0],gt[1],gt[2],arrayTopCords[1],gt[4],gt[5]])
    outRaster.SetProjection(proj)
    outband = outRaster.GetRasterBand(1)
    outband.SetNoDataValue(0)
    outband.WriteArray(outArray)
start = time. time()
flowDirFile="/home/bharath/Documents/catchmentDelineation/data/testDir.tif"
outFile="/home/bharath/Documents/catchmentDelineation/data/testWSnumba.tif"
# segFile="D:\NHP\dev_catchment\data\\testSeg.tif"
point=(77.20723842,19.95570563)
compBuf=1
raster=gdal.Open(flowDirFile)
gt=raster.GetGeoTransform()
proj=raster.GetProjection()
relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point)
# print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
end = time. time()
print(end - start)
