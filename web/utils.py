from django.db import connection


def get_admin_dashboard_stats(data_filter):
    date_from = data_filter['from']
    date_to = data_filter['to']
    with connection.cursor() as cursor:
        query = """
           SELECT COUNT(*)
           FROM (SELECT DISTINCT ru.id
           FROM recordings_record AS rr
           FULL JOIN recordings_user ru ON ru.id = rr.user_id
           WHERE rr.record_date >= (%s) AND rr.record_date <= (%s)) as a
           """
        cursor.execute(query, (date_from, date_to))
        active_users = cursor.fetchall()
        query = """
                   SELECT COUNT(*)
                   FROM recordings_record AS rr
                   WHERE rr.record_date >= (%s) AND rr.record_date <= (%s) 
                   """
        cursor.execute(query, (date_from, date_to))
        recordings_made = cursor.fetchall()
        query = """
                           SELECT rc.category_name, COUNT(rr.id) AS used_total
                           FROM recordings_record AS rr
                           INNER JOIN recordings_category rc on rc.id = rr.category_id
                           WHERE rr.record_date >= (%s) AND rr.record_date <= (%s)
                           GROUP BY rc.category_name
                           ORDER BY  used_total
                           LIMIT 5
                           """
        cursor.execute(query, (date_from, date_to))
        popular_categories = cursor.fetchall()
        connection.cursor().close()

    results = {'popular_categories': popular_categories, 'active_users': active_users[0][0],
               'recordings_made': recordings_made[0][0]}
    return results
