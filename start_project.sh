#!/bin/bash
# grant execute permissions at the first time: chmod +x start_project.sh


# Get the directory where the script is located ane set it as PYTHONPATH
export PYTHONPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

echo "PYTHONPATH is set to: $PYTHONPATH"

# Optionally, activate a virtual environment
# source "${SCRIPT_DIR}/venv/bin/activate"