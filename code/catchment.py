import gdal
import numpy
from os import listdir,path,walk,system,sys
from math import ceil,floor
"""
    77.26744369,20.06364357
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
    releventArray=raster.ReadAsArray(arrayBounds[0],arrayBounds[1],arrayBounds[2]-arrayBounds[0],arrayBounds[3]-arrayBounds[1])
    return releventArray,arrayBounds,pointPixel
def Core(array,point):
    outArray=numpy.zeros()
    toChklist=[point]
    addedList=[point]
    for eachPoint in toChklist:
        for i in [(1,1),(1,0),(1,-1),(0,1),(0,-1),(-1,-1),(-1,0),(-1,1)]:
            print array[int(point[1]+i[1]),int(point[0]+i[0])],i
        # toChklist.remove(eachPoint)
    # while True:
    #     pixelsIn=len(addedList)
    #     for eachPoint in toChklist:
    #         for i in range(0,8):
    #             array[point[1],point[0]]
    #         toChklist.remove(eachPoint)
def getCatchment(gt,array,arrayBounds,pointPixel):
    arrayTopCords=[gt[0]+arrayBounds[0]*gt[1],gt[3]+arrayBounds[1]*gt[5]]
    pointPixel=[pointPixel[0]-arrayBounds[0],pointPixel[1]-arrayBounds[1]]
    Core(array,pointPixel)
flowDirFile="D:\NHP\dev_catchment\data\\testDir.tif"
segFile="D:\NHP\dev_catchment\data\\testSeg.tif"
point=(77.2735235,19.9672154)
compBuf=0.1
raster=gdal.Open(flowDirFile)
gt=raster.GetGeoTransform()
relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point)
# print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
getCatchment(gt,array,arrayBounds,pointPixel)
