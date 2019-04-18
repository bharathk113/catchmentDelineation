import gdal
import numpy
raster=gdal.Open(r'F:\cartodem\cartomos.tif')
rasterProj=raster.GetProjection()
rasterGt=raster.GetGeoTransform()
# print rasterProj,rasterGt
boundary=(77.124999,20.25,81.375,15.75)
boundaryPixs=(int((boundary[0]-rasterGt[0])/rasterGt[1]),int((boundary[1]-rasterGt[3])/rasterGt[5]),int((boundary[2]-rasterGt[0])/rasterGt[1]),int((boundary[3]-rasterGt[3])/rasterGt[5]))
# boundaryPreciseCoords=(boundaryPixs[0]*rasterGt[1]+rasterGt[0],rasterGt[3]+boundaryPixs[1]*rasterGt[5],boundaryPixs[2]*rasterGt[1]+rasterGt[0],rasterGt[3]+boundaryPixs[3]*rasterGt[5])
# print boundaryPixs,boundaryPreciseCoords,boundaryPixs[0],boundaryPixs[1],boundaryPixs[2]-boundaryPixs[0],boundaryPixs[1]-boundaryPixs[0]
# array=raster.ReadAsArray(boundaryPixs[0],boundaryPixs[1],boundaryPixs[2]-boundaryPixs[0],boundaryPixs[3]-boundaryPixs[1])
driver = gdal.GetDriverByName('HFA')
# outRaster = driver.Create(r'E:\CDEM\cdemtelangana.img', boundaryPixs[2]-boundaryPixs[0], boundaryPixs[3]-boundaryPixs[1], 1, gdal.GDT_UInt16)
parts=10
pixInPart=[int((boundaryPixs[2]-boundaryPixs[0])/parts),int((boundaryPixs[3]-boundaryPixs[1])/parts)]
for i in range(0,parts):
    for j in range(0,parts):
        if i==0 and j==0:
            a=boundaryPixs[0]+i*pixInPart[0]
            b=boundaryPixs[1]+j*pixInPart[1]
            c=pixInPart[0]+50
            d=pixInPart[1]+50
        elif 0<i<parts-1 and j==0:
            a=boundaryPixs[0]+i*pixInPart[0]-50
            b=boundaryPixs[1]+j*pixInPart[1]
            c=pixInPart[0]+100
            d=pixInPart[1]+50
        elif i==parts-1 and j==0:
            a=boundaryPixs[0]+i*pixInPart[0]-50
            b=boundaryPixs[1]+j*pixInPart[1]
            c=boundaryPixs[2]-boundaryPixs[0]-i*pixInPart[0]+50
            d=pixInPart[1]+50
        elif i==0 and 0<j<parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]
            b=boundaryPixs[1]+j*pixInPart[1]-50
            c=pixInPart[0]+50
            d=pixInPart[1]+100
        elif 0<i<parts-1 and 0<j<parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]-5
            b=boundaryPixs[1]+j*pixInPart[1]-5
            c=pixInPart[0]+100
            d=pixInPart[1]+100
        elif i==parts-1 and 0<j<parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]-50
            b=boundaryPixs[1]+j*pixInPart[1]-50
            c=boundaryPixs[2]-boundaryPixs[0]-i*pixInPart[0]+50
            d=pixInPart[1]+100
        elif i==0 and j==parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]
            b=boundaryPixs[1]+j*pixInPart[1]-50
            c=pixInPart[0]+50
            d=boundaryPixs[3]-boundaryPixs[1]-j*pixInPart[1]+50
        elif 0<i<parts-1 and j==parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]-50
            b=boundaryPixs[1]+j*pixInPart[1]-50
            c=pixInPart[0]+100
            d=boundaryPixs[3]-boundaryPixs[1]-j*pixInPart[1]+50
        elif i==parts-1 and j==parts-1:
            a=boundaryPixs[0]+i*pixInPart[0]-50
            b=boundaryPixs[1]+j*pixInPart[1]-50
            c=boundaryPixs[2]-boundaryPixs[0]-i*pixInPart[0]+50
            d=boundaryPixs[3]-boundaryPixs[1]-j*pixInPart[1]+50
        array=raster.ReadAsArray(a,b,c,d)
        # driver = gdal.GetDriverByName('HFA')
        outRaster = driver.Create(r'E:\CDEM\cdemtelangana'+str(i)+str(j)+'.img', array.shape[1], array.shape[0], 1, gdal.GDT_UInt16)
        outband = outRaster.GetRasterBand(1)
        outband.WriteArray(array)
        boundaryPreciseCoords=(a*rasterGt[1]+rasterGt[0],rasterGt[3]+b*rasterGt[5],(a+c)*rasterGt[1]+rasterGt[0],rasterGt[3]+(b+d)*rasterGt[5])
        outRaster.SetGeoTransform((boundaryPreciseCoords[0],rasterGt[1],0,boundaryPreciseCoords[1],0,rasterGt[5]))
        outRaster.SetProjection(rasterProj)
        print array.shape,outRaster.RasterXSize,outRaster.RasterYSize,pixInPart
        # outband.WriteArray(array,i*pixInPart[0],j*pixInPart[1])
        print "part",i,j,"is done"
#outRaster = driver.Create(join(outFolder,outFilename), columns, rows, len(bandNames), gdal.GDT_UInt16)
