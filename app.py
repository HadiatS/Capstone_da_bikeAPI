import sqlite3
import requests
from tqdm import tqdm

from flask import Flask, request
import json 
import numpy as np
import pandas as pd

app = Flask(__name__) 

@app.route('/')
@app.route('/home/')
def home():
    return 'Capston API Algoritma'

@app.route('/json', methods=['POST']) 
def json_example():
    
    req = request.get_json(force=True) # Parse the incoming json data as Dictionary
    
    name = req['name']
    age = req['age']
    address = req['address']
    
    return (f'''Hello {name}, your age is {age}, and your address in {address}
            ''')

@app.route('/sample', methods=['POST']) 
def sample_data():
    
    input_data = request.get_json(force=True) # Parse the incoming json data as Dictionary
    specified_date = input_data['period']
    conn = make_connection()
    query = f""" SELECT * FROM trips WHERE start_time LIKE '{specified_date}%' """
    selected_data = pd.read_sql_query(query, conn)
    # Make the aggregate
    result = selected_data.groupby('start_station_id').agg({
    'bikeid' : 'count','duration_minutes' : 'mean'})

    return result.to_json()



##mendapatkan data semua station
@app.route('/stations/')
def route_all_stations():
    conn = make_connection()
    stations = get_all_stations(conn)
    return stations.to_json()

@app.route('/stations/<station_id>')
def route_stations_id(station_id):
    conn = make_connection()
    station = get_station_id(station_id, conn)
    return station.to_json()

#@app.route('/<status_station>')
@app.route('/stations/status/<status_station>')
def route_status_station(status_station):
    conn = make_connection()
    status = get_station_status(status_station, conn)
    return status.to_json()

##dapatkan data semua trips
@app.route('/trips/')
def route_all_trips():
    conn = make_connection()
    trips = get_all_trips(conn)
    return trips.to_json()

@app.route('/trips/<trips_id>')
def route_trips_id(trips_id):
    conn = make_connection()
    trips = get_trips_id(trips_id, conn)
    return trips.to_json()   
 
## mendaptakan tahun dari trips ####
@app.route('/trips/tahun/<tahun>')
def route_trips_year(tahun):
    conn = make_connection()
    years = get_trip_year(tahun, conn)
    return years.to_json() 
#Get all table
@app.route('/join/') 
def route_all_table():
    conn = make_connection()
    join = get_all_table( conn)
    return join.to_json() 

@app.route('/average_duration/')
def route_average_duration():
    conn = make_connection()
    average = average_duration(conn)
    return average.to_json()

@app.route('/trips/average_duration/<bike_id>')
def route_average_duration_bikeid(bike_id):
    conn = make_connection()
    average = average_duration_bike_id(bike_id,conn)
    return average.to_json()

#tugas
@app.route('/total_status_year/')
def route_total_status_year():
    conn = make_connection()
    total = total_status_year(conn)
    return total.to_json()

@app.route('/total_status_year/<tahun>/', defaults={'status_station1': None})
@app.route ('/total_status_year/<tahun>/<status_station1>')
def route_total_status_station_peryear(tahun,status_station1):
    if status_station1 == None:
        status_station1 =""
    conn = make_connection()
    total1 = total_status_station_peryear(tahun,status_station1,conn)
    return total1.to_json()

#### INPUT STATION #####
@app.route('/stations/add', methods=['POST']) 
def route_add_station():
    # parse and transform incoming data into a tuple as we need
    data = pd.Series(eval(request.get_json(force=True)))
    data = tuple(data.fillna('').values)  
    conn = make_connection()
    result = insert_into_stations(data, conn)
    return result

#### INPUT TRAINS ####
@app.route('/trips/add', methods=['POST']) 
def route_add_trips():
    # parse and transform incoming data into a tuple as we need 
    data = pd.Series(eval(request.get_json(force=True)))
    data = tuple(data.fillna('').values)
    conn = make_connection()
    result = insert_into_trips(data, conn)
    return result

#TUGAS POST INPUT
@app.route('/data', methods=['POST']) 
def get_data_bulan():
    input_data = request.get_json(force=True)
    spesifik_tahun = input_data['tahun']
    conn = make_connection()
    query = f""" 
            SELECT * FROM trips 
            WHERE start_time LIKE '{spesifik_tahun}%'
    """
    data_tahun = pd.read_sql_query(query,conn,parse_dates=['start_time'])
    data_tahun['bulan'] = data_tahun['start_time'].dt.month_name()
    result = data_tahun.pivot_table(index ='bulan',
                                columns='subscriber_type',
                                values='start_station_name',
                                aggfunc='count',
                                fill_value=0)
    result['Total']=result.iloc[1].sum()
    return result.to_json()


#### FUNCTION #####
def make_connection():
    connection = sqlite3.connect('austin_bikeshare.db')
    return connection

### FUNCTION STATIONS #####
def get_all_stations(conn):
    query = f"""SELECT * FROM stations"""
    result = pd.read_sql_query(query, conn)
    return result

def get_station_id(station_id, conn):
    query = f"""SELECT * FROM stations WHERE station_id IS {station_id}"""
    result = pd.read_sql_query(query, conn)
    print(result)
    return result 
#NEW COBA
def get_station_status(status_station,conn):
    query = f""" 
        SELECT * FROM stations WHERE status IS '{status_station}'
        """
    result = pd.read_sql_query(query,conn)
    return result

### FUNCTION TRIPS ####
def get_all_trips(conn):
    query = f"""SELECT * FROM trips """
    result = pd.read_sql_query(query,conn)
    print(result.head(5))
    return result

def get_trips_id(trips_id,conn):
    query = f"""SELECT * FROM trips WHERE id = {trips_id}"""
    result = pd.read_sql_query(query, conn)
    print(result)
    return result
# NEW DATA FUNCTION STATIC AND DYNAMIC
def get_trip_year(tahun, conn):
    query = f""" SELECT * FROM trips WHERE start_time LIKE '{tahun}%' """
    result = pd.read_sql_query(query,conn)
    print(result)
    return result 

# togehter
def get_all_table(conn):
    query = """ 
        SELECT trips.*, stations.status, stations.power_type,stations.modified_date
        FROM trips
        LEFT JOIN stations
            ON trips.start_station_id = stations.station_id
        """
    result = pd.read_sql_query(query,conn)
    return result

def average_duration(conn):
    query = """ 
        SELECT bikeid, AVG(duration_minutes) as 'AVERAGE_DURATION'
        FROM trips
        GROUP BY bikeid
        ORDER BY AVERAGE_DURATION DESC
        """
    result = pd.read_sql_query(query,conn)
    return result
#hitung jumlah status station per year
def total_status_year(conn):
    query = """ 
        SELECT SUBSTR(REPLACE(start_time, ' UTC', ''), 1, 4) AS year, status, COUNT(stations.status) as 'TotalStatus'
        FROM trips
        LEFT JOIN stations
            ON trips.start_station_id = stations.station_id
        GROUP BY year, status
        ORDER BY year, status """
    result = pd.read_sql_query(query,conn)
    return result

def total_status_station_peryear(tahun,status_station1,conn):
    query = f""" 
        SELECT SUBSTR(REPLACE(start_time, ' UTC', ''), 1, 4) AS year, status, COUNT(stations.status) as 'TotalStatus'
        FROM trips
        LEFT JOIN stations
            ON trips.start_station_id = stations.station_id
        GROUP BY year,status
            HAVING (year IS '{tahun}') AND  (status = '{status_station1}' OR '{status_station1}' = '' OR '{status_station1}' IS NULL)
         """
    result = pd.read_sql_query(query,conn)
    return result

def average_duration_bike_id(bike_id,conn):
    query = f""" 
        SELECT bikeid, AVG(duration_minutes) as 'AVERAGE_DURATION'
        FROM trips
        WHERE bikeid IS '{bike_id}'
        """
    result = pd.read_sql_query(query,conn)
    return result

### FUNGSI input
def insert_into_stations(data, conn):
    query = f"""INSERT INTO stations values {data}"""
    try:
        conn.execute(query)
    except:
        return 'Error'
    conn.commit()
    return 'OK'

def insert_into_trips(data, conn):
    query = f"""INSERT INTO trips values {data}"""
    try:
        conn.execute(query)
    except:
        return 'Error'
    conn.commit()
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, port=5000)