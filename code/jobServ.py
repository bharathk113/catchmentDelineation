from subprocess import Popen
import time
import fetchJobs
if __name__=="__main__":
    numJobs=0
    limit=4
    out=[0 for i in range(0,limit)]
    err=[0 for i in range(0,limit)]
    while True:
        if numJobs<limit:
            out[numJobs],err[numJobs]=Popen([ 'python', 'D:\\NHP\dev\\tankCatchment\\fetchJobs.py'])
            print out,err
            numJobs+=1
        time.sleep(1)
        print 1,numJobs,out,err
