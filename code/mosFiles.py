"""
Original    :cdemtelangana
Name        :cdemtelangana
Source      :Z:/Nizamsagar_donotdelete/telangana_reference/telanganaDem/cdemtelangana.img
Provider    :gdal
CRS         :EPSG:4326 - WGS 84 - Geographic
Extent      :77.1249074074074059,15.7500000000000000 : 81.3750000000000000,20.2500000000000000
Unit        :degrees
Width       :45901
Height      :48600
Data type   :UInt16 - Sixteen bit unsigned integer
GDAL Driver Description:HFA
GDAL Driver Metadata:Erdas Imagine Images (.img)
Dataset Description:Z:/Nizamsagar_donotdelete/telangana_reference/telanganaDem/cdemtelangana.img
Compression :
Band 1      :LAYER_TYPE=athematic
STATISTICS_MAXIMUM=1152
STATISTICS_MEAN=246.41306893227
STATISTICS_MINIMUM=0
STATISTICS_STDDEV=174.356663947
More information:Dimensions:X: 45901 Y: 48600   Bands: 1  Origin: 77.1249,20.25    Pixel Size:9.25926e-5,-9.25926e-5

"""
import gdal
import numpy
from os import listdir,path,walk,system,sys
def filesinsidefolder(myPath,form):
    fileNames=[]
    xmlFiles=[]
    for dirpath, dirnames, filenames in walk(myPath):
        for filename in [f for f in filenames if form in f]:
            if '.aux' in filename:
                pass
            elif '.tfw' in filename:
                pass
            elif '.img' in filename:
                pass
            else:
                xmlFiles.append(path.join(dirpath, filename))
                fileNames.append(filename)
    return xmlFiles,fileNames
if __name__=="__main__":
    inFilesFolder=r"Z:\\Nizamsagar_donotdelete\\telangana_reference\\telanganaDem\\outcdem"
    form=sys.argv[1]
    outFile = r"Z:\\Nizamsagar_donotdelete\\telangana_reference\\telanganaDem\\outcdem\\telangana.img"
    outFile=outFile[:-4]+str(form)[:-1]+'.img'
    totCols,totRows=45901,48600
    driver = gdal.GetDriverByName('HFA')
    if form=='bin':
        outRaster = driver.Create(outFile, totCols,totRows, 1, gdal.GDT_Byte, ['NBITS=1'])
    else:
        outRaster = driver.Create(outFile, totCols,totRows, 1, gdal.GDT_UInt16)
    outband = outRaster.GetRasterBand(1)
    fullFilePaths,fileNames=filesinsidefolder(inFilesFolder,form)
    parts=10
    buf=150
    pixInPart=[int(totCols/parts),int(totRows/parts)]
    # print fullFilePaths
    for eachFile in fullFilePaths:
        if form=='bin':
            i,j=eachFile[-9:-7]
        else:
            i,j=eachFile[-6:-4]
        print "mosaicing",eachFile
        i,j=(int(i),int(j))
        if i==0 and j==0:
            a=0
            b=0
            c=buf
            d=buf
        elif 0<i<parts-1 and j==0:
            a=-1*buf
            b=0
            c=2*buf
            d=buf
        elif i==parts-1 and j==0:
            a=-1*buf
            b=0
            c=buf
            d=buf
        elif i==0 and 0<j<parts-1:
            a=0
            b=-1*buf
            c=buf
            d=2*buf
        elif i==0 and j==parts-1:
            a=0
            b=-1*buf
            c=buf
            d=buf
        elif i<parts-1 and j<parts-1:
            a=-1*buf
            b=-1*buf
            c=2*buf
            d=2*buf
        elif i==parts-1 and j<parts-1:
            a=-1*buf
            b=-1*buf
            c=buf
            d=2*buf
        elif i<parts-1 and j==parts-1:
            a=-1*buf
            b=-1*buf
            c=2*buf
            d=buf
        elif i==parts-1 and j==parts-1:
            a=-1*buf
            b=-1*buf
            c=buf
            d=buf
        raster=gdal.Open(eachFile)
        rows=raster.RasterYSize
        cols=raster.RasterXSize
        print a,b,c,d,cols-(c),rows-(d),rows,cols
        array=raster.ReadAsArray(-1*a,-1*b,cols-(c),rows-(d))
        noData=raster.GetRasterBand(1).GetNoDataValue()
        if noData==65535:
            array=array+1
        print "writing",i,j
        outband.WriteArray(array,i*pixInPart[0],j*pixInPart[1])
    outRaster.SetGeoTransform([77.1249074074074059,raster.GetGeoTransform()[1],raster.GetGeoTransform()[2],20.2500000000000000,raster.GetGeoTransform()[4],raster.GetGeoTransform()[5]])
    outRaster.SetProjection(raster.GetProjection())
    outband.SetNoDataValue(0)
    # for i in range(0,parts):
    #     for j in range(0,parts):
    #         if i==0 and j==0:
            #     a=boundaryPixs[0]+i*pixInPart[0]
            #     b=boundaryPixs[1]+j*pixInPart[1]
            #     c=pixInPart[0]+5
            #     d=pixInPart[1]+5
            # elif 0<i<parts-1 and j==0:
            #     a=boundaryPixs[0]+i*pixInPart[0]-5
            #     b=boundaryPixs[1]+j*pixInPart[1]
            #     c=pixInPart[0]+10
            #     d=pixInPart[1]+5
            # elif i==0 and 0<j<parts-1:
            #     a=boundaryPixs[0]+i*pixInPart[0]
            #     b=boundaryPixs[1]+j*pixInPart[1]-5
            #     c=pixInPart[0]+5
            #     d=pixInPart[1]+10
            # elif i<parts-1 and j<parts-1:
            #     a=boundaryPixs[0]+i*pixInPart[0]-5
            #     b=boundaryPixs[1]+j*pixInPart[1]-5
            #     c=pixInPart[0]+10
            #     d=pixInPart[1]+10
            # elif i==parts-1 and j<parts-1:
            #     a=boundaryPixs[0]+i*pixInPart[0]-5
            #     b=boundaryPixs[1]+j*pixInPart[1]-5
            #     c=boundaryPixs[2]-boundaryPixs[0]-i*pixInPart[0]+5
            #     d=pixInPart[1]+10
            # elif i<parts-1 and j==parts-1:
            #     a=boundaryPixs[0]+i*pixInPart[0]-5
            #     b=boundaryPixs[1]+j*pixInPart[1]-5
            #     c=pixInPart[0]+10
            #     d=boundaryPixs[3]-boundaryPixs[1]-j*pixInPart[1]+5
            # elif i==parts-1 and j==parts-1:
            #     a=boundaryPixs[0]+i*pixInPart[0]-5
            #     b=boundaryPixs[1]+j*pixInPart[1]-5
            #     c=boundaryPixs[2]-boundaryPixs[0]-i*pixInPart[0]+5
            #     d=boundaryPixs[3]-boundaryPixs[1]-j*pixInPart[1]+5
            # array=raster.ReadAsArray(a,b,c,d)
    #         # driver = gdal.GetDriverByName('HFA')
    #
    #         outband.WriteArray(array)
    #         boundaryPreciseCoords=(a*rasterGt[1]+rasterGt[0],rasterGt[3]+b*rasterGt[5],(a+c)*rasterGt[1]+rasterGt[0],rasterGt[3]+(b+d)*rasterGt[5])
    #         outRaster.SetGeoTransform((boundaryPreciseCoords[0],rasterGt[1],0,boundaryPreciseCoords[1],0,rasterGt[5]))
    #         outRaster.SetProjection(rasterProj)
    #         print array.shape,outRaster.RasterXSize,outRaster.RasterYSize,pixInPart
    #         # outband.WriteArray(array,i*pixInPart[0],j*pixInPart[1])
    #         print "part",i,j,"is done"
