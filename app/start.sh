#!/bin/sh

INITIAL_FILE="/var/app/initial"
HAS_GUNICORN=$(command -v gunicorn)

if [ ! -e "$INITIAL_FILE" ]  || [ -z "$HAS_GUNICORN" ]; then
    echo "Installing packages...."
    pip3 install -r requirements.txt
    touch $INITIAL_FILE
    echo "Finished install packages...."
fi

gunicorn -w 4 -b 0.0.0.0:5000 app:app
