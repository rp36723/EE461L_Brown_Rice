#!/bin/bash

# Get the current working directory
root="$(pwd)"

# Start the React frontend
cd "$root/client"
npm start &

# Activate the virtual environment for the Flask backend
cd "$root/server"
source venv/bin/activate

# Run the Flask backend
python app.py

