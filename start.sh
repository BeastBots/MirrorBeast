#!/bin/bash

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Activate virtual environment if exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the update script and main program
python3 update.py && python3 -m bot
