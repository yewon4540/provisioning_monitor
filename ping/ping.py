from sshtunnel import SSHTunnelForwarder
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import ipaddress
import pymysql
import os
import re

load_dotenv()

# db 정보
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_name = os.getenv('DB_NAME')

ssh_conf = os.getenv('SSH_CONF')
ssh_path = os.getenv('SSH_PATH')

# 터널 설정
server = SSHTunnelForwarder(
    ssh_address_or_host=ssh_conf,  # ssh config 에 정의된 host alias
    ssh_config_file=ssh_path,
    remote_bind_address=('127.0.0.1', 8827),  # SMM 내부의 MariaDB 포트
    local_bind_address=('127.0.0.1', 4257)    # 로컬에서 사용할 포트
)

server.start()

conn = pymysql.connect(
    host='127.0.0.1',
    port=4257,
    user=db_user,
    password=db_pass,
    database=db_name
)

cursor = conn.cursor()

# 공유기 리스트 가져오기
cursor.execute("SELECT router_ip FROM router_config")
router_list = [row[0] for row in cursor.fetchall()]


# 정규식 패턴: 타임스탬프 + IP + TTL + 시간
pattern = r'\[(\d+\.\d+)]\s+\d+ bytes from ([\d.]+):.*ttl=(\d+).*time=([\d.]+) ms'

log_dir = "error_log"

for host in router_list:
    # print(f"{host} 시작!")
    try:
        result = subprocess.run(
            ["ping", "-c", "3", "-W", "1", "-i", "1", "-D", host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        stdout_output = result.stdout

        for match in re.finditer(pattern, stdout_output):
            timestamp_, router, ttl_, duration_ = match.groups()

            timestamp = float(timestamp_)
            converted = datetime.fromtimestamp(timestamp)
            readable_time = converted.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

            ttl = int(ttl_)
            duration = float(duration_)

            # DB에 삽입
            cursor.execute('''
                INSERT INTO ping_log (datetime, router, ttl, during)
                VALUES (%s, %s, %s, %s)
            ''', (readable_time, router, ttl, duration))

            print(f"[✅ 저장됨] {readable_time} {router} TTL={ttl} time={duration}ms")

    except subprocess.CalledProcessError as e:
        # now = datetime.now().strftime("%Y%m%d_%H%M%S")
        # log_file = os.path.join(log_dir, f"{host.replace('.', '_')}_{now}.log")
        # with open(log_file, "w") as f:
            # f.write("===== STDOUT =====\n")
            # f.write(e.stdout or "")
            # f.write("\n===== STDERR =====\n")
            # f.write(e.stderr or "")
        cursor.execute('''
            INSERT INTO error_monitor (date, router)
            VALUES (%s, %s)
        ''', (readable_time, host))
        print(f"[⚠️ Ping 실패] {readable_time} {host}")

    # print(f"{host} 끝!")
conn.commit()
cursor.close()
conn.close()
server.stop()

# # 그 외 네트워크 체크 명령어
# nmap -sP 10.40.1.0/24
# nmap -O 10.40.1.0
# ping 
