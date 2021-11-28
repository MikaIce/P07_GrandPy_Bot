""" This module will lauch the app """
# !/usr/bin/python3
# -*- coding: Utf-8 -*
from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 80))