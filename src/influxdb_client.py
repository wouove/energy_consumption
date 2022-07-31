import sys
import datetime
import time

import requests
from influxdb import InfluxDBClient

DBNAME = 'house_measurements'
MEASUREMENT = 'energy_measurements'


class InfluxdbClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connect_db()

    def connect_db(self):
        '''connect to the database, and create it if it does not exist'''
        global client
        print('connecting to database: {}:{}'.format(self.host, self.port))
        client = InfluxDBClient(self.host, self.port, retries=5, timeout=1)
        self.wait_for_server(self.host, self.port)
        create = False
        if not self.db_exists():
            create = True
            print('creating database...')
            client.create_database(DBNAME)
        else:
            print('database already exists')
        client.switch_database(DBNAME)
        # if not create and reset:
        #     client.delete_series(measurement=MEASUREMENT)

    def wait_for_server(self, host, port, nretries=5):
        '''wait for the server to come online for waiting_time, nretries times.'''
        url = 'http://{}:{}'.format(host, port)
        waiting_time = 1
        for i in range(nretries):
            try:
                requests.get(url)
                return
            except requests.exceptions.ConnectionError:
                print('waiting for', url)
                time.sleep(waiting_time)
                waiting_time *= 2
                pass
        print('cannot connect to', url)
        sys.exit(1)

    def db_exists(self):
        '''returns True if the database exists'''
        dbs = client.get_list_database()
        for db in dbs:
            if db['name'] == DBNAME:
                return True
        return False

    def store_measurement(self, measurement):
        '''insert dummy measurements to the db.
        nmeas = 0 means : insert measurements forever.
        '''
        i = 0
        if nmeas == 0:
            nmeas = sys.maxsize
        for i in range(nmeas):
            x = i / 10.
            y = math.sin(x)
            data = [{
                'measurement': measurement,
                'time': datetime.datetime.now(),
                'tags': {
                    'x': x
                },
                'fields': {
                    'y': y
                },
            }]
            client.write_points(data)
            pprint.pprint(data)
            time.sleep(1)
