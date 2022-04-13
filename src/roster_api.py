from fastapi import FastAPI, HTTPException, Request
import json
from roster_database import RosterDatabase
from playhouse.shortcuts import model_to_dict
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

@app.get("/roster_entry/{id}", response_class=HTMLResponse)
async def show_roster_entry(request: Request, id: str):
    entry = RosterDatabase().get_roster_entry_by_id(id)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Roster entry with id {id} not found")
    return templates.TemplateResponse("roster_entry.html", {"request": request, "roster_entry": entry})