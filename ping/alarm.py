import pymysql
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import requests

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT")),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME")
}

LAMBDA_ALERT_URL = os.getenv("LAMBDA_URL")

# 무한 호출 방지용 쿨다운(마지막 호출 시점 기록)파일 생성 / 기준 시간 : 30분
COOLDOWN_FILE = "last_alert.log"
COOLDOWN_MINUTES = 30

def is_cooldown():
    if not os.path.exists(COOLDOWN_FILE):
        return False

    with open(COOLDOWN_FILE, "r") as f:
        last_time_str = f.read().strip()

    try:
        last_time = datetime.fromisoformat(last_time_str)
    except ValueError:
        return False

    elapsed = datetime.now() - last_time
    minutes_elapsed = int(elapsed.total_seconds() // 60)

    if elapsed < timedelta(minutes=COOLDOWN_MINUTES):
        print(f"[⏳ 유예 중] 마지막 경보 이후 {minutes_elapsed}분 경과됨.")
        print(f"마지막 경보 시각 : {last_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return True

    return False


def update_cooldown():
    with open(COOLDOWN_FILE, "w") as f:
        f.write(datetime.now().isoformat())

        
def check_alert_conditions():
    conn = pymysql.connect(**DB_CONFIG)
    cursor = conn.cursor()

    now = datetime.now()
    window_start = (now - timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')

    # 응답 없는 공유기
    cursor.execute('''
        SELECT rc.router_ip
        FROM router_config rc
        LEFT JOIN ping_log pl
        ON rc.router_ip = pl.router AND pl.datetime > %s
        WHERE pl.router IS NULL
    ''', (window_start,))
    no_response = cursor.fetchall()

    # duration > 100ms 만 기록된 공유기
    cursor.execute('''
        SELECT pl.router
        FROM ping_log pl
        WHERE pl.datetime > %s
        GROUP BY pl.router
        HAVING COUNT(*) = SUM(pl.during > 100)
    ''', (window_start,))
    slow_response = cursor.fetchall()

    cursor.close()
    conn.close()

    dead_count = len(no_response)
    slow_count = len(slow_response)

    alerts = []
    if dead_count >= 10:
        alerts.append(f"❌ [작동 불량] 최근 10분간 응답 없음 공유기: {dead_count}대")
    if slow_count >= 10:
        alerts.append(f"🐢 [속도 저하] 최근 10분간 느린 응답 공유기: {slow_count}대")

    return alerts

def send_alerts(alerts):
    if not alerts:
        print("[✅ 정상] 알림 조건 없음")
        return

    message = "\n".join(alerts)
    print("[🚨 경보 발생]", message)

    payload = {"message": message}
    try:
        response = requests.post(LAMBDA_ALERT_URL, json=payload)
        print("[📤 전송 완료]", response.status_code)
    except Exception as e:
        print("[❌ 전송 실패]", e)

if __name__ == "__main__":
    if is_cooldown():
        print("전송 생략.")
    else:
        alerts = check_alert_conditions()  # 테스트 시 24시간
        if alerts:
            send_alerts(alerts)
            update_cooldown()
