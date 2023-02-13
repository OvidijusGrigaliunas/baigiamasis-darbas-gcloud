from django.db import connection
from google.cloud import storage
import csv


def download_data():
    bucket = "baigiamasis-darbas-373611.appspot.com"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob('data/user_data.csv')
    with connection.cursor() as cursor:
        query = """
        SELECT *
        FROM recordings_record AS rr
        FULL JOIN recordings_record_data rrd ON rr.id = rrd.record_id
        FULL JOIN recordings_category rc ON rc.id = rr.category_id
        FULL JOIN recordings_user ru ON ru.id = rr.user_id
        """
        cursor.execute(query)
        results = cursor.fetchall()
        connection.cursor().close()
        with blob.open("w") as csvfile:
            filewriter = csv.writer(csvfile)
            for row in results:
                filewriter.writerow(row)
            csvfile.close()


