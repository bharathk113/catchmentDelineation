import gdal,ogr,osr,time,os,json
from os import path
from catchment import getCatchment,readReleventArray
def singlepoint(point=None):
    bufIncrement=0.25
    start = time. time()
    flowDirFile="D:/TWRIS/tankCatchment/jangaondrinagedirection.tif"
    if point is None:
        point=(79.17955793,17.90319865)
    outFile=path.join(path.dirname(flowDirFile),str(point[0])+'_'+str(point[1])+'.tif')
    # outFile="D:/TWRIS/tankCatchment/catchments_Jangaon/testWSnumba.tif"
    compBuf=1
    raster=gdal.Open(flowDirFile)
    gt=raster.GetGeoTransform()
    proj=raster.GetProjection()
    relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point,compBuf)
    # print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
    result=getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
    while result==-1:
        compBuf+=bufIncrement
        relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point,compBuf)
        result=getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
        if compBuf>1:
            print "Please select a smaller stream or a coarser resolution DEM for same point,skipping point..."
            break
    if compBuf>1.5:
        continue
    outRast = gdal.Open(outFile)
    outBand =  outRast.GetRasterBand(1)
    proj=outRast.GetProjection()
    srs=osr.SpatialReference()
    srs.ImportFromWkt(proj)
    outShapefile=outFile[:-4]+'.geojson'
    outDriver = ogr.GetDriverByName("GeoJSON")
    # Remove output shapefile if it already exists
    if os.path.exists(outShapefile):
        outDriver.DeleteDataSource(outShapefile)
    # Create the output shapefile
    outDataSource = outDriver.CreateDataSource(outShapefile)
    outLayer = outDataSource.CreateLayer("polygon", srs, geom_type=ogr.wkbPolygon)
    # Add an ID field
    idField = ogr.FieldDefn("DN", ogr.OFTInteger)
    outLayer.CreateField(idField)
    print "polygonizing..."
    gdal.Polygonize(outBand, None , outLayer, 0, [], callback=None )
    # j=0
    # for feat in outLayer:
    #     if feat.GetField("DN")!=1:
    #         outLayer.DeleteFeature(j)
    #     j+=1
    # outLayer.ResetReading()
    outDataSource=None
    outLayer=None
    with open(outShapefile,'r') as jsonfile:
        jsondata=json.load(jsonfile)
    for i in range(len(jsondata["features"])):
        if jsondata['features'][i]['properties']['DN']==0:
            jsondata['features'].pop(i)
    with open(outShapefile,'w') as jsonfile:
        json.dump(jsondata,jsonfile)
    print "polygonized. :)"
    outBand=None
    outRast=None
    if os.path.exists(outFile):
        os.remove(outFile)
    if os.path.exists(outShapefile):
        os.remove(outShapefile)
    print i,"points completed"
    i+=1
    end = time. time()
    print(end - start)
singlepoint()
