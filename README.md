# OceanEye

OceanEye is a dependency-light prototype for AI-assisted marine oil-spill investigation. It demonstrates the complete chain from satellite evidence through drift reconstruction, source estimation, AIS correlation, explainable candidate ranking and an evidence graph.

## Run the frontend

Open `index.html` directly in a browser. The Demo Mode is self-contained and needs no API keys or live datasets.

## Run the optional FastAPI backend

```powershell
python -m pip install fastapi uvicorn python-multipart
python -m uvicorn backend.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Example endpoints include `/investigations`, `/preprocess`, `/spill/detect`, `/drift/reconstruct`, `/source/estimate`, `/vessels`, `/ais/correlate`, `/candidates/rank`, and `/evidence/{investigation_id}`.

## Notes

- All displayed investigation outputs are explicitly demo/simulation outputs.
- The candidate score indicates likelihood from available evidence, not legal or scientific proof of responsibility.
- Replace the in-memory demo data in `backend/main.py` with PostGIS-backed services and real satellite/AIS adapters when integrating live sources.
