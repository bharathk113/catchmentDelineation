#!/usr/bin/python
import psycopg2
def get_latlon(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * from data_updation where status=0 order by created_at")
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchall()

        # while row is not None:
        #     print(row)
        #     row = cur.fetchone()
        try:
            lat,lon=float(row[0].split(',')[1]),float(row[0].split(',')[0])
        except:
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
        params = {'database': 'snowmelt','user': 'postgres','password': 'postgres','host': '192.168.192.109','port': 5432}
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
    if latlon!=None:
        return latlon[0],latlon[1]
    else:
        return "Error retriving Latlon from db"
if __name__ == '__main__':
    connect()
