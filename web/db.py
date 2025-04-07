import pymysql
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

def get_router_status():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # router_config + ping_log 조인하여 최신 ping 데이터 조회
    cursor.execute('''
        SELECT rc.router_ip, rc.router_name, rc.location, 
               pl.datetime, pl.ttl, pl.during
        FROM router_config rc
        LEFT JOIN (
            SELECT router, MAX(datetime) AS latest_time
            FROM ping_log
            GROUP BY router
        ) latest ON rc.router_ip = latest.router
        LEFT JOIN ping_log pl ON pl.router = latest.router AND pl.datetime = latest.latest_time
        ORDER BY rc.location ASC
    ''')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    result = []
    for row in rows:
        ip, name, location, dt_raw, ttl, during = row

        status = "✅" if ttl is not None else "⚠️"

        if dt_raw:
            dt_obj = dt_raw if isinstance(dt_raw, datetime) else datetime.strptime(dt_raw, "%Y-%m-%d %H:%M:%S.%f")
            formatted_time = dt_obj.strftime("%Y년 %m월 %d일 %H시%M분")
        else:
            formatted_time = "-"

        result.append({
            "ip": ip,
            "name": name,
            "location": location,
            "datetime": formatted_time,
            "ttl": ttl,
            "during": during,
            "status": status
        })

    return result
