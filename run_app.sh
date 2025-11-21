#!/bin/bash
echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Starting Mac Program Cleaner..."
python3 main.py
