#!/bin/bash
set -e

echo "--- [1] Проверка кода через Bandit ---"
bandit -r app.py

echo "--- [2] Сборка Docker-образа ---"
docker build -t devsecops-agent .

echo "--- [3] Проверка образа через Trivy ---"
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image --severity HIGH,CRITICAL --exit-code 1 devsecops-agent

echo "--- Успех, проверка пройдена! ---"
