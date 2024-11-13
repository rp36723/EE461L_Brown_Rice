#!/bin/bash

# Get the current working directory
root="$(pwd)"

# Start and install the React frontend
echo "React Frontend"
cd "$root/client"

# Check if install
if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

# start
npm start &

# Flask backend
echo "Flask Backend"
cd "$root/server"

# Check
if [ ! -d "venv" ]; then
  echo "Setting up Python virtual environment and installing dependencies..."
  python -m venv venv
fi

# vm
source venv/bin/activate

if [ ! -f ".env" ]; then
  echo "Creating .env file from .env_template..."
  cp .env_template .env
fi

# requirement
pip install -r requirements.txt

python app.py
