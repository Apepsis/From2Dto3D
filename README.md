# From2Dto3D

From2Dto3D is a local-first computer-vision prototype for turning a guided set of room photos into a panorama, a spatial room graph, and an interactive 3D inspection scene.

It is intentionally designed as a **real engineering MVP**, not a fake “AI 3D” demo. The backend measures blur, detects ORB features, estimates image overlap, stitches compatible frames with OpenCV, and produces a confidence report. The web client guides capture, shows quality feedback, visualizes the reconstructed room and lets users build connections between rooms.

## What works now

- Guided photo capture/upload with capture coverage and orientation hints.
- Per-image sharpness checks (variance of Laplacian).
- ORB feature extraction and pairwise overlap/match scoring.
- OpenCV panorama stitching with a transparent failure state.
- Equirectangular panorama viewer and interactive Three.js room scene.
- Local project persistence, room topology graph and exportable project JSON.
- Quantitative processing report: success, frame count, blur, feature count, overlap, processing time and confidence.

## Deliberately not claimed as complete

NeRF/3D Gaussian Splatting, metric depth, full SLAM and automatic floorplans require calibrated capture and trained models. The app exposes the data and extension points needed for them; it does not pretend they are already solved.

## Run locally

```bash
docker compose up --build
```

Open `http://localhost:5173`. The API documentation is at `http://localhost:8000/docs`.

For development without Docker:

```bash
cd api && python -m venv .venv && .venv/bin/pip install -r requirements.txt && uvicorn app.main:app --reload
cd web && npm install && npm run dev
```

## Architecture

```text
Browser capture/upload → React capture guidance → FastAPI CV pipeline
                                        ↓                    ↓
                                  room graph ← report + panorama
                                        ↓
                              Three.js / 360 panorama viewer
```

## Evaluation

Use the report for every capture session. A valid experiment records: frame count, mean sharpness, median adjacent overlap, stitch success, processing latency, and manual panorama-quality rating. Keep failed sessions: they are essential evidence for improving capture guidance.

## Privacy

Images are processed in-memory for the request and are not stored by the API. The browser saves only project metadata in local storage unless the user exports it.
