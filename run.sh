#!/bin/bash

# 사용법 안내
if [ -z "$1" ]; then
  echo "❗ 사용법: ./run.sh <port>"
  exit 1
fi

PORT=$1
LOGFILE="flask_$PORT.log"

# 백그라운드 실행 & 로그 저장
nohup python3 app.py "$PORT" > "$LOGFILE" 2>&1 &

