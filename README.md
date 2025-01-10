# Capstone_da_bikeAPI

1. Aplikasi Home dengan return home atau /

INPUT:
2. sample : /json untuk input data latihan (contoh)
3. Input '/sampe' input data berupa period : 2015-08
4. @app.route('/stations/add', methods=['POST']) 
5. @app.route('/trips/add', methods=['POST']) 

STATIC:
1. Mendapatkan data semua stations dengan '/stations/'


4. @app.route('/trips/') -> dapatkan data tabel semua trips
5. @app.route('/join/') gabungkan data table trips dan stations
6. @app.route('/average_duration/') -> data durasi -> task sample 

DYNAMIC
1. Mendapatkan '/stations/<station_id>'
2. Mendapatkan data dari status stations dengan mengetikan '/stations/status/<status_station> -> active,closed (return berupa tabel)
3. @app.route('/trips/<trips_id>')
4. @app.route('/trips/tahun/<tahun>') -> /trips/tahun/ 2015-2021 -> return berbentuk tabel 
5. @app.route('/trips/average_duration/<bike_id>')


#tugas
@app.route('/total_status_year/') -> static untuk mencari nilai status setiap tahun keseluruhan
@app.route('/total_status_year/<tahun>/', defaults={'status_station1': None}) -> dynamic hanya tahun-tahun tertentu
@app.route ('/total_status_year/<tahun>/<status_station1>') -> lanjutan diatas jika dipilih tahun dan spesifikasi dari status station (closed,active)

#TUGAS POST INPUT
@app.route('/data', methods=['POST']) 
    masukan data JSON tahun:2015 (misal) maka akan mendapatkan nilai dalam tahun tersebut data perbulannya untuk jenis subscriber dan total perbulannya.
