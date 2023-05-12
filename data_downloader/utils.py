from django.db import connection
from google.cloud import storage
import csv


def download_data(from_date, to_date):
    bucket = "baigiamasis-darbas-373611.appspot.com"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob('data/user_data.csv')
    with connection.cursor() as cursor:
        query = """
        SELECT ru.id, ru.birthdate, ru.height, ru.weight, rr.id, rr.record_date, rr.data_interval,
        rc.category_name, rrd.id, rrd.gyro_x, rrd.gyro_y, rrd.gyro_z, rrd.accel_x, rrd.accel_y, 
        rrd.accel_z,rrd. magnet_x, rrd.magnet_y, rrd.magnet_z, rrde.id, 
        rrde.gyro_x, rrde.gyro_y, rrde.gyro_z, rrde.accel_x, rrde.accel_y, rrde.accel_z, 
        rrde.magnet_x, rrde.magnet_y, rrde.magnet_z, rrde.temp, rrde.pressure
        FROM recordings_record AS rr
        FULL JOIN recordings_record_data rrd ON rr.id = rrd.record_id
        FULL JOIN recordings_record_data_extra rrde ON rr.id = rrde.record_id
        FULL JOIN recordings_category rc ON rc.id = rr.category_id
        FULL JOIN recordings_user ru ON ru.id = rr.user_id
        WHERE rr.record_date >= (%s) AND rr.record_date <= (%s)
        """
        cursor.execute(query, (from_date, to_date))
        results = cursor.fetchall()
        connection.cursor().close()
        with blob.open("w") as csvfile:
            data_name_row = [
                'user_id',
                'user_birthdate',
                'user_height',
                'user_weight',
                'record_id',
                'record_date',
                'data_interval',
                'category_name',
                'phone_data_id',
                'phone_gyro_x',
                'phone_gyro_y',
                'phone_gyro_z',
                'phone_accel_x',
                'phone_accel_y',
                'phone_accel_z',
                'phone_magnet_x',
                'phone_magnet_y',
                'phone_magnet_z',
                'wearable_sensor_data_id',
                'wearable_sensor_gyro_x',
                'wearable_sensor_gyro_y',
                'wearable_sensor_gyro_z',
                'wearable_sensor_accel_x',
                'wearable_sensor_accel_y',
                'wearable_sensor_accel_z',
                'wearable_sensor_magnet_x',
                'wearable_sensor_magnet_y',
                'wearable_sensor_magnet_z',
                'wearable_sensor_temp',
                'wearable_sensor_pressure'
            ]
            filewriter = csv.writer(csvfile)
            filewriter.writerow(data_name_row)
            for row in results:
                filewriter.writerow(row)
            csvfile.close()
