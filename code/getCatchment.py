"""


                    author: Bharath Reddy K


                    For the first time, Create a grassdb using GRASS GIS GUI
                    Add grass path, location, mapset and grass version in the code as entered during the beginning of grass GUI session.

                                            inputs: threshold-to search for streams in units of the map,
                                            points file-the location of all outlet points,
                                            streams raster from qgis- to locate nearby streams.


"""
from osgeo import gdal,ogr,osr
from os import listdir,path,walk,system
import os,numpy
import sys
import subprocess

# define GRASS Database
# add your path to grassdata (GRASS GIS database) directory
gisdb = "C:\\Users\\Bharath\\Documents\\TWRIS\\tankCatchment\\GRASS"
# gisdb = str(sys.argv[1])
# the following path is the default path on MS Windows
# gisdb = os.path.join(os.path.expanduser("~"), "Documents/grassdata")

# specify (existing) Location and Mapset
location = "loc4326"
mapset = "PERMANENT"
# location = str(sys.argv[2])
# mapset = str(sys.argv[3])
# path to the GRASS GIS launch script
# we assume that the GRASS GIS start script is available and on PATH
# query GRASS itself for its GISBASE
# (with fixes for specific platforms)
# needs to be edited by the user
grass7bin = 'grass74'
# grass7bin = str(sys.argv[4])
if sys.platform.startswith('win'):
    # MS Windows
    grass7bin = r'C:/Program Files/QGIS 3.2/bin/grass74.bat'
    # grass7bin = str(sys.argv[5])
    # uncomment when using standalone WinGRASS installer
    # grass7bin = r'C:\Program Files (x86)\GRASS GIS 7.2.0\grass76.bat'
    # this can be avoided if GRASS executable is added to PATH
elif sys.platform == 'darwin':
    # Mac OS X
    # TODO: this have to be checked, maybe unix way is good enough
    grass7bin = '/Applications/GRASS/GRASS-7.2.app/'

# query GRASS GIS itself for its GISBASE
startcmd = [grass7bin, '--config', 'path']
try:
    p = subprocess.Popen(startcmd, shell=False,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
except OSError as error:
    sys.exit("ERROR: Cannot find GRASS GIS start script"
             " {cmd}: {error}".format(cmd=startcmd[0], error=error))
if p.returncode != 0:
    sys.exit("ERROR: Issues running GRASS GIS start script"
             " {cmd}: {error}"
             .format(cmd=' '.join(startcmd), error=err))
gisbase = out.strip(os.linesep)

# set GISBASE environment variable
os.environ['GISBASE'] = gisbase

# define GRASS-Python environment
grass_pydir = os.path.join(gisbase, "etc", "python")
sys.path.append(grass_pydir)

# import (some) GRASS Python bindings
import grass.script as gscript
import grass.script.setup as gsetup

# launch session
rcfile = gsetup.init(gisbase, gisdb, location, mapset)

# example calls
gscript.message('Current GRASS GIS 7 environment:')
print gscript.gisenv()

gscript.message('Available raster maps:')
for rast in gscript.list_strings(type='raster'):
    print rast

gscript.message('Available vector maps:')
for vect in gscript.list_strings(type='vector'):
    print vect
flowDirFile=r"C:\\Users\\Bharath\\Documents\\TWRIS\\CheckDams\\kmDrainageDirection.tif"
# flowDirFile=str(sys.argv[6])
computationBuffer=3
# computationBuffer=float(sys.argv[7])
floDirRaster=gdal.Open(flowDirFile)
gt=floDirRaster.GetGeoTransform()
print gt
gscript.run_command('r.external',input=flowDirFile,output='flowDirFile',overwrite='True')
pointsFile=r"C:\\Users\\Bharath\\Documents\\TWRIS\\CheckDams\\Krishnamiddle_Str_4to8_outletpointsnearest.csv"
# pointsFile=str(sys.argv[8])
delimtter=','
with open(pointsFile,'r') as f:
    data=f.read()
data=data.split('\n')
i=1
for eachline in data:
    if eachline!="":
        outFile=path.join(path.dirname(pointsFile),eachline.split(delimtter)[0][:6]+'_'+eachline.split(delimtter)[1][:6]+'.tif')
        nB=str(gt[3])
        sB=str(gt[3]+gt[5]*floDirRaster.RasterYSize+gt[5])
        eB=str(gt[0]+gt[1]*floDirRaster.RasterXSize+gt[1])
        wB=str(gt[0])
        pointCoordinates=[float(eachline.split(',')[0]),float(eachline.split(',')[1])]
        regionBounds=[pointCoordinates[0]-computationBuffer,pointCoordinates[1]+computationBuffer,pointCoordinates[0]+computationBuffer,pointCoordinates[1]-computationBuffer]
        if regionBounds[1]<float(nB):
            nB=regionBounds[1]
        if regionBounds[0]>float(wB):
            wB=regionBounds[0]
        if regionBounds[2]<float(eB):
            eB=regionBounds[2]
        if regionBounds[3]>float(sB):
            sB=regionBounds[3]
        gscript.run_command('g.region',n=str(nB), s=str(sB), e=str(eB), w=str(wB), res=str(gt[1]))
        gscript.run_command('r.water.outlet', input='flowDirFile',coordinates=eachline, output='outFile', overwrite='True')
        gscript.run_command('g.region', raster='outFile')
        gscript.run_command('r.out.gdal' , input='outFile', output=outFile, type='Byte', overwrite='True')

        # gscript.run_command('r.to.vect', flags='sv', input='outFile', output='vectOut', type='area',overwrite='True')
        # gscript.run_command('v.out.ogr', flags='e', input='vectOut', type='area', output=outFile[:-4]+'.shp',overwrite='True')
        # gscript.run_command('g.remove' , flags='f' , type='vector' , name='vectOut')
        outRast = numpy.sum(gdal.Open(outFile))
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
        print "polygonized. :)"
        outBand=None
        outRast=None
        if os.path.exists(outFile):
            os.remove(outFile)
        print i,"points completed"
        i+=1
# clean up at the end
# gsetup.cleanup()
