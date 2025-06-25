#!/bin/bash

# 사용법 안내
if [ -z "$1" ]; then
  echo "❗ 사용법: ./run.sh <port>"
  exit 1
fi

PORT=$1

# Python 스크립트 실행
python3 app.py "$PORT"

