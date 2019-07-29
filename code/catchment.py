"""


                    author: Bharath Reddy K


                                            inputs: computation region,
                                            points file-the location of all outlet points,
                                            streams raster from qgis- to locate nearby streams.


"""
import gdal,osr,ogr,os,numba,numpy,sys
from os import listdir,path,walk,system,sys
from math import ceil,floor
import time
from numba import jit
"""
    Requires above mentioned packages
"""
def readReleventArray(raster,gt,point,compBuf):
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
    print (arrayBounds[0],arrayBounds[1],arrayBounds[2]-arrayBounds[0],arrayBounds[3]-arrayBounds[1])
    print (pointPixel)
    releventArray=raster.ReadAsArray(arrayBounds[0],arrayBounds[1],arrayBounds[2]-arrayBounds[0]-1,arrayBounds[3]-arrayBounds[1]-1)
    # print (releventArray)
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
        if eachPoint[0]<0 or eachPoint[0]>=inArray.shape[0] or eachPoint[1]<0 or eachPoint[1]>=inArray.shape[1]:
            print ("The buffer region is insufficient, increasing the buffer..")
            outArray=numpy.full(inArray.shape,-1.0)
            return outArray
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
def getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj):
    arrayTopCords=[gt[0]+arrayBounds[0]*gt[1],gt[3]+arrayBounds[1]*gt[5]]
    pointPixel=(pointPixel[0]-arrayBounds[0],pointPixel[1]-arrayBounds[1])
    outArray=Core(relArray,pointPixel)
    if outArray.any()==-1:
        return -1
    driver = gdal.GetDriverByName('GTIFF')
    outRaster = driver.Create(outFile, relArray.shape[1],relArray.shape[0], 1, gdal.GDT_Byte, ['NBITS=1'])
    outRaster.SetGeoTransform([arrayTopCords[0],gt[1],gt[2],arrayTopCords[1],gt[4],gt[5]])
    outRaster.SetProjection(proj)
    outband = outRaster.GetRasterBand(1)
    outband.SetNoDataValue(0)
    outband.WriteArray(outArray)
    return 0
##############################Enable this for Single known point
# start = time. time()
# flowDirFile="/home/bharath/Documents/catchmentDelineation/data/testDir.tif"
# point=(77.20723842,19.95570563)
# outFile="/home/bharath/Documents/catchmentDelineation/data/testWSnumba.tif"
# compBuf=1
# raster=gdal.Open(flowDirFile)
# gt=raster.GetGeoTransform()
# proj=raster.GetProjection()
# relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point)
# # print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
# getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
# end = time. time()
# print(end - start)
##############################Enable this for CSV mode with multiple points/single point
# flowDirFile="Z:\\Nizamsagar_donotdelete\\telangana_reference\\telanganaDem\\outcdem\\telanganadrain.img"
# # flowDirFile=sys.argv[1]
# pointsFile=r"D:\\TWRIS\\tankCatchment\\catchments_Jangaon\\jangaonTanksNearest.csv"
#
# delimtter=','
# with open(pointsFile,'r') as f:
#     data=f.read()
# data=data.split('\n')
# i=1
# for eachline in data:
#     if eachline!="":
#         start = time. time()
#         outFile=path.join(path.dirname(pointsFile),eachline.split(delimtter)[0][:6]+'_'+eachline.split(delimtter)[1][:6]+'.tif')
#         point=(float(eachline.split(delimtter)[0]),float(eachline.split(delimtter)[1]))
#         compBuf=0.25
#         raster=gdal.Open(flowDirFile)
#         gt=raster.GetGeoTransform()
#         proj=raster.GetProjection()
#         relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point)
#         # print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
#         getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
#         outRast = gdal.Open(outFile)
#         outBand =  outRast.GetRasterBand(1)
#         proj=outRast.GetProjection()
#         srs=osr.SpatialReference()
#         srs.ImportFromWkt(proj)
#         outShapefile=outFile[:-4]+'.geojson'
#         outDriver = ogr.GetDriverByName("GeoJSON")
#         # Remove output shapefile if it already exists
#         if os.path.exists(outShapefile):
#             outDriver.DeleteDataSource(outShapefile)
#         # Create the output shapefile
#         outDataSource = outDriver.CreateDataSource(outShapefile)
#         outLayer = outDataSource.CreateLayer("polygon", srs, geom_type=ogr.wkbPolygon)
#         # Add an ID field
#         idField = ogr.FieldDefn("DN", ogr.OFTInteger)
#         outLayer.CreateField(idField)
#         print "polygonizing..."
#         gdal.Polygonize(outBand, None , outLayer, 0, [], callback=None )
#         j=0
#         for feat in outLayer:
#             if feat.GetField("DN")!=1:
#                 outLayer.DeleteFeature(j)
#             j+=1
#         outLayer.ResetReading()
#         print "polygonized. :)"
#         outBand=None
#         outRast=None
#         if os.path.exists(outFile):
#             os.remove(outFile)
#         print i,"points completed"
#         i+=1
#         end = time. time()
#         print(end - start)
##############################
