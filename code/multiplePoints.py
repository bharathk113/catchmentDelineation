import gdal,ogr,osr,time,os,json
from os import path
from catchment import getCatchment,readReleventArray


flowDirFile="D:\\TWRIS\\tankCatchment\\jangaondrinagedirection.tif"
# flowDirFile=sys.argv[1]
pointsFile=r"D:\\TWRIS\\tankCatchment\\catchments_Jangaon\\jangaonTanksNearest.csv"

delimtter=','
with open(pointsFile,'r') as f:
    data=f.read()
data=data.split('\n')
i=1
for eachline in data:
    if eachline!="":
        start = time. time()
        outFile=path.join(path.dirname(pointsFile),eachline.split(delimtter)[0][:6]+'_'+eachline.split(delimtter)[1][:6]+'.tif')
        point=(float(eachline.split(delimtter)[0]),float(eachline.split(delimtter)[1]))
        compBuf=0.25
        raster=gdal.Open(flowDirFile)
        gt=raster.GetGeoTransform()
        proj=raster.GetProjection()
        relArray,arrayBounds,pointPixel=readReleventArray(raster,gt,point,compBuf)
        # print (gdal.Open(segFile)).ReadAsArray(int(pointPixel[0]),int(pointPixel[1]),1,1)
        getCatchment(gt,relArray,arrayBounds,pointPixel,outFile,proj)
        outRast = gdal.Open(outFile)
        outBand =  outRast.GetRasterBand(1)
        proj=outRast.GetProjection()
        srs=osr.SpatialReference()
        srs.ImportFromWkt(proj)
        outShapefile=outFile[:-4]+'.shp'
        outDriver = ogr.GetDriverByName("ESRI Shapefile")
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
        j=0
        for feat in outLayer:
            if feat.GetField("DN")!=1:
                outLayer.DeleteFeature(j)
            j+=1
        outLayer.ResetReading()
        print "polygonized. :)"
        outBand=None
        outRast=None
        if os.path.exists(outFile):
            os.remove(outFile)
        print i,"points completed"
        i+=1
        end = time. time()
        print(end - start)
##############################
