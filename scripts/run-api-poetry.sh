#!/bin/bash

export DIRECTORY_ROSTER=/home/tom/development/personal/jmri-roster-data/roster
export ROSTER_DATABASE_LOCATION=/home/tom/development/personal/jmri-roster-data/roster.db
export DEBUG=False

cd ../src
poetry run uvicorn roster_api:app --reload