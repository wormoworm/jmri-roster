from fastapi import FastAPI, HTTPException
import json
from roster_database import RosterDatabase
from playhouse.shortcuts import model_to_dict
from datetime import datetime

app = FastAPI()

@app.get("/api/v2/roster")
def get_roster():
    entries = RosterDatabase().get_all_roster_entries()
    entries_array = []
    for entry in entries:
        entries_array.append(model_to_dict(entry, backrefs=True))
    return {"roster": entries_array}


@app.get("/api/v2/roster_entry/{id}")
def get_roster_entry(id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return {"roster_entry": model_to_dict(entry, backrefs=True)}