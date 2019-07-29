#!/usr/bin/python
import psycopg2
def get_latlon(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT jobid,ST_X(geom),ST_Y(geom) from catchment.basetable where status='QUEUED' order by created_at")
        # print("The number of parts: ", cur.rowcount)
        row = cur.fetchall()

        # while row is not None:
        #     print(row)
        #     row = cur.fetchone()
        try:
            # print (row,type(row[1][1]))
            lat,lon=float(row[0][1]),float(row[0][0])
            # cur.execute("UPDATE catchment.basetable SET status='PROCESSING' where status='QUEUED' and jobid={}",row[0][0])
            # lat,lon=float(row[0][1].split(',')[1]),float(row[0][1].split(',')[0])
        except:
            print("LatLonNotCorrect")
            return "LatLonNotCorrect"
        cur.close()
        return lat,lon

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
def connect():
    """ Connect to the PostgreSQL database server """
    #latlon='78.66210937500001,18.656654486540006'
    conn = None
    try:
        # read connection parameters
        params = {'database': 'postgis','user':'bharath','password':'@@Fr86tz','host': 'localhost','port': 5432}
        # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        # conn=psycopg2.connect(dbname="snowmelt", user="postgres", password="postgres", host = '192.168.192.109', port = 5432)
        conn = psycopg2.connect(**params)
        latlon=get_latlon(conn)
        #update_twris_data(conn,latlon)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            return latlon
    latlon=None
    if latlon!=None:
        return latlon[0],latlon[1]
    else:
        return "Error retriving Latlon from db"
if __name__ == '__main__':
    connect()
