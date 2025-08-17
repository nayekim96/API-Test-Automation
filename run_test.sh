#!/bin/bash

# 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# pytest 실행
pytest tests/

# 가상 환경 비활성화
deactivate