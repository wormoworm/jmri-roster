#!/bin/bash

export DIRECTORY_ROSTER=/home/tom/development/personal/jmri-roster-data/roster
export MONITOR_CHANGES=True
export ROSTER_DATABASE_LOCATION=/home/tom/development/personal/jmri-roster-data/roster.db
export DEBUG=False

poetry run python -u ../src/run_importer.py