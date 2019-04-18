
"""


author: Bharath Reddy


This code works only if all the points lie inside of the raster(stream segments). No exceptions handles otherwise.
Both the raster and shapefile should be of same projection.

                        inputs: threshold, points file, streams raster from qgis


# TODO: Handle the points that don't have streams in given threshold


"""
from osgeo import gdal,ogr
from os import listdir,path,walk
import sys,math,time,numpy
from numba import jit
def getXY(lyr,gt):
    coords=[]
    for feat in lyr:
        multipoint = feat.GetGeometryRef()
        geom = multipoint.GetGeometryRef(0) ##########For multipoint
        mx=geom.GetX()
        my=geom.GetY()
        px = int((mx - gt[0]) / gt[1])
        py = int((my - gt[3]) / gt[5])
        coords.append([px,py])
    return coords
def coreNearest(arr,xcenter,ycenter):
    newArr=numpy.full(arr.shape,numpy.inf)
    for i in range(0,arr.shape[0]):
        for j in range(0,arr.shape[1]):
            if arr[i][j]==1:
                newArr[i][j]=((i-ycenter)**2)+((j-xcenter)**2)
    point=numpy.unravel_index(newArr.argmin(), newArr.shape)
    if newArr[point[0],point[1]]==numpy.inf:
        point=(ycenter,xcenter)
    return (point[1],point[0])
def coreLowest(arr,demArr,xcenter,ycenter):
    newArr=numpy.full(arr.shape,numpy.inf)
    for i in range(0,arr.shape[0]):
        for j in range(0,arr.shape[1]):
            if arr[i][j]!=0:
                newArr[i][j]=demArr[i][j]
    point=numpy.unravel_index(newArr.argmin(), newArr.shape)
    if newArr[point[0],point[1]]==numpy.inf:
        point=(ycenter,xcenter)
    return (point[1],point[0])
def searchRaster(coords,raster,demRaster,threshold,gt):
    readPixelsX,readPixelsY=int(2*threshold/gt[1]),int(-2*threshold/gt[5])
    modCoords=[]
    for eachPoint in coords:
        # print eachPoint[0]-int(readPixelsX/2),eachPoint[1]-int(readPixelsY/2),readPixelsX,readPixelsY
        if eachPoint[0]-int(readPixelsX/2)>=0 and eachPoint[1]-int(readPixelsY/2) and eachPoint[0]-int(readPixelsX/2)+readPixelsX<raster.RasterXSize and eachPoint[1]-int(readPixelsY/2)+readPixelsY<raster.RasterYSize:
            searchArray=raster.ReadAsArray(eachPoint[0]-int(readPixelsX/2),eachPoint[1]-int(readPixelsY/2),readPixelsX,readPixelsY)
            #######################################################################################################################################################
            #################Enable this for nearest stream
            # temp=coreNearest(searchArray,int(readPixelsX/2),int(readPixelsY/2))
            #################Enable this for lowest point on nearby streams
            demArray=demRaster.ReadAsArray(eachPoint[0]-int(readPixelsX/2),eachPoint[1]-int(readPixelsY/2),readPixelsX,readPixelsY)
            temp=coreLowest(searchArray,demArray,int(readPixelsX/2),int(readPixelsY/2))
            #######################################################################################################################################################
            temp=[temp[0]+eachPoint[0]-int(readPixelsX/2),temp[1]+eachPoint[1]-int(readPixelsY/2)]
            temp=[gt[0]+temp[0]*gt[1]+gt[1]/2,gt[3]+temp[1]*gt[5]+gt[5]/2]
            print temp
            modCoords.append(temp)
    return modCoords
def main():
    streamsFile=r"C:\\Users\\Bharath\\Documents\\TWRIS\\tankCatchment\\telanganaDem\\telanganabi.img"
    demFile=r"C:\\Users\\Bharath\\Documents\\TWRIS\\CheckDams\\kmStreamSegments.img"
    pointsFile=r"D:\\delete\\Kamareddy_tanks.shp"
    streamsRaster=gdal.Open(streamsFile)
    demRaster=gdal.Open(demFile)
    gt=streamsRaster.GetGeoTransform()
    drv = ogr.GetDriverByName("ESRI Shapefile")
    inpData = ogr.Open(pointsFile)
    inpLayer = inpData.GetLayer(0)
    coords = getXY(inpLayer,gt)
    threshold=0.0005 #mapunits
    modCoords=searchRaster(coords,streamsRaster,demRaster,threshold,gt)
    with open(pointsFile[:-4]+'nearest.csv','w+') as f:
        for eachPoint in modCoords:
            f.write(str(eachPoint[0])+','+str(eachPoint[1])+'\n')


if __name__=="__main__":
    main()
