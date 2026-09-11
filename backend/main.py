from datetime import datetime
from pathlib import Path
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title='OceanEye Demo API', version='0.9.4')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

class Investigation(BaseModel):
    name: str = 'Bay of Bengal spill event'
    date: str = '2026-04-17'
    area: str = '12.48N, 78.21E'
    mode: str = 'demo'

class DriftRequest(BaseModel):
    latitude: float = Field(12.4821, ge=-90, le=90)
    longitude: float = Field(78.2145, ge=-180, le=180)
    hours: int = Field(24, ge=1, le=168)

VESSELS = [
    {'name': 'MV Ocean Star', 'mmsi': '419001842', 'imo': '9821047', 'score': 92.4},
    {'name': 'Sea Voyager', 'mmsi': '419007311', 'imo': '9384210', 'score': 84.7},
    {'name': 'Blue Horizon', 'mmsi': '419003082', 'imo': '9701183', 'score': 72.3},
    {'name': 'Pacific Trader', 'mmsi': '419006194', 'imo': '9517720', 'score': 61.8},
    {'name': 'Kaveri Dawn', 'mmsi': '419002771', 'imo': '9255104', 'score': 53.6},
]

@app.get('/health')
def health():
    return {'status': 'ok', 'mode': 'demo', 'time': datetime.utcnow().isoformat() + 'Z'}

@app.post('/investigations')
def create_investigation(investigation: Investigation):
    return {'id': 'OE-26-0417', 'status': 'created', 'investigation': investigation}

@app.post('/data/upload')
def upload_data(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail='A filename is required')
    return {'dataset': file.filename, 'status': 'staged', 'quality': 92.1, 'demo': True}

@app.post('/preprocess')
def preprocess():
    return {'status': 'complete', 'satellite_images': 12, 'ais_records': 18542, 'missing_ais_percent': 4.2, 'ocean_records': 1250}

@app.post('/spill/detect')
def detect_spill():
    return {'status': 'complete', 'confidence': 94.2, 'area_km2': 18.6, 'centroid': {'latitude': 12.4821, 'longitude': 78.2145}, 'demo': True}

@app.post('/drift/reconstruct')
def reconstruct_drift(request: DriftRequest):
    return {'status': 'complete', 'hours': request.hours, 'uncertainty_km': 6.4, 'current': '1.8 kn NE', 'wind': '12 kn WNW', 'demo': True}

@app.post('/source/estimate')
def estimate_source():
    return {'latitude': 12.4821, 'longitude': 78.2145, 'time': '2026-04-16T20:30:00Z', 'confidence': 87, 'uncertainty_km': 6.4}

@app.get('/vessels')
def vessels() -> List[dict]:
    return VESSELS

@app.post('/ais/correlate')
def correlate_ais():
    return {'status': 'complete', 'nearby_vessels': 8, 'candidates': 5, 'records': 18542}

@app.post('/candidates/rank')
def rank_candidates():
    return {'status': 'complete', 'candidates': sorted(VESSELS, key=lambda vessel: vessel['score'], reverse=True), 'explainable': True}

@app.get('/evidence/{investigation_id}')
def evidence(investigation_id: str):
    return {'investigation_id': investigation_id, 'nodes': ['satellite', 'spill', 'drift', 'source', 'ais', 'candidate_score'], 'status': 'complete'}

@app.get('/investigations/{investigation_id}')
def get_investigation(investigation_id: str):
    if investigation_id != 'OE-26-0417':
        raise HTTPException(status_code=404, detail='Investigation not found')
    return {'id': investigation_id, 'status': 'complete', 'mode': 'demo', 'top_candidate': VESSELS[0], 'limitations': ['AIS gaps', 'weather uncertainty', 'satellite look-alikes']}
