from os import listdir,path,walk,system
import time
def filesinsidefolder(myPath,form):
    fileNames=[]
    xmlFiles=[]
    for dirpath, dirnames, filenames in walk(myPath):
        for filename in [f for f in filenames if form in f]:
            if '.aux' in filename:
                pass
            else:
                xmlFiles.append(path.join(dirpath, filename))
                fileNames.append(filename)
    return xmlFiles,fileNames
if __name__=='__main__':
    time.sleep(5*3600)
    fullfilepaths,filenames=filesinsidefolder(r'Z:\Nizamsagar_donotdelete\telangana_reference\telanganaDem\outcdem','stream_')
    for eachFile in fullfilepaths:
        # print "executing",'python C:\\Users\\Bharath\\Documents\\NHP\\dev\\tankCatchment\\streamsBin.py '+eachFile
        system('python C:\\Users\\Bharath\\Documents\\NHP\\dev\\tankCatchment\\streamsBin.py '+eachFile)
    system('python C:\\Users\\Bharath\\Documents\\NHP\\dev\\tankCatchment\\mosFiles.py bin_')
    system('python C:\\Users\\Bharath\\Documents\\NHP\\dev\\tankCatchment\\mosFiles.py drain_')
