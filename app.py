import sys
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return f"Flask 서버가 {port} 포트에서 실행 중입니다.✌️"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("❗ 사용법: python app.py <port>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        app.run(host='0.0.0.0', port=port)
    except ValueError:
        print("❗ 포트는 숫자로 입력해야 합니다.")
        sys.exit(1)
