#!/bin/sh

echo 'Start Asman'
# ls -al
python -m celery -A src.background.app.BACKGROUND_APP flower &
# python -m celery -A src.gateway.app.BACKGROUND_APP flower &
python src/background/app.py &
python src/gateway/app.py
echo 'Asman UP!'
