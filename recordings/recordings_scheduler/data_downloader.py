from apscheduler.schedulers.background import BackgroundScheduler
from django.db import connection
import csv


def start():
    download_data()
    scheduler = BackgroundScheduler()
    if len(scheduler.get_jobs()) != 0:
        scheduler.remove_all_jobs()
    scheduler.add_job(download_data, trigger='cron', hour='5', minute='5', timezone="EET", id="test",
                      replace_existing=True)
    scheduler.start()


def download_data():
    with connection.cursor() as cursor:
        query = "SELECT * FROM user_data_user"
        cursor.execute(query)
        results = cursor.fetchall()
        with open('user_downloaded_data/downloaded_user_data.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile)
            header = ("id", "height", "weight", "birthdate", "user_id")
            filewriter.writerow(header)
            for row in results:
                filewriter.writerow(row)
            csvfile.close()
