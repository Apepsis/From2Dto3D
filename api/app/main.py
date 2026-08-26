from __future__ import annotations

import time
from typing import Any

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="From2Dto3D CV API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


def decode(upload: UploadFile, raw: bytes) -> np.ndarray:
    image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(422, f"{upload.filename or 'file'} is not a decodable image")
    return image


def inspect(image: np.ndarray) -> tuple[float, int, Any, Any]:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    keypoints, descriptors = cv2.ORB_create(nfeatures=1800).detectAndCompute(gray, None)
    return sharpness, len(keypoints), keypoints, descriptors


def pair_overlap(left: Any, right: Any) -> tuple[int, float]:
    if left is None or right is None:
        return 0, 0.0
    matches = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(left, right)
    good = [match for match in matches if match.distance < 55]
    return len(good), round(min(1.0, len(good) / 110.0), 3)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    if len(files) < 2:
        raise HTTPException(422, "Upload at least two photos to assess overlap.")
    if len(files) > 60:
        raise HTTPException(422, "Maximum 60 photos per job.")
    started = time.perf_counter()
    decoded = [decode(upload, await upload.read()) for upload in files]
    inspected = [inspect(image) for image in decoded]
    overlaps = [pair_overlap(inspected[i][3], inspected[i + 1][3]) for i in range(len(inspected) - 1)]
    sharpness = [round(item[0], 1) for item in inspected]
    features = [item[1] for item in inspected]
    return {
        "frames": len(decoded), "sharpness": sharpness, "features": features,
        "adjacent_overlaps": [{"matches": m, "score": s} for m, s in overlaps],
        "mean_sharpness": round(float(np.mean(sharpness)), 1),
        "median_overlap": round(float(np.median([s for _, s in overlaps])), 3),
        "capture_ready": float(np.median([s for _, s in overlaps])) >= .18 and float(np.mean(sharpness)) >= 45,
        "processing_ms": round((time.perf_counter() - started) * 1000),
    }


@app.post("/stitch")
async def stitch(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    if len(files) < 2:
        raise HTTPException(422, "Upload at least two photos to stitch.")
    started = time.perf_counter()
    decoded = [decode(upload, await upload.read()) for upload in files]
    resized = [cv2.resize(image, (0, 0), fx=min(1, 1600 / image.shape[1]), fy=min(1, 1600 / image.shape[1])) for image in decoded]
    status, panorama = cv2.Stitcher_create(cv2.Stitcher_PANORAMA).stitch(resized)
    if status != cv2.Stitcher_OK:
        return {"success": False, "reason": "No reliable panorama. Retake photos with 30–50% overlap, consistent exposure and visible texture.", "opencv_status": int(status), "processing_ms": round((time.perf_counter() - started) * 1000)}
    ok, encoded = cv2.imencode(".jpg", panorama, [cv2.IMWRITE_JPEG_QUALITY, 91])
    if not ok:
        raise HTTPException(500, "Panorama encoding failed.")
    import base64
    return {"success": True, "panorama": "data:image/jpeg;base64," + base64.b64encode(encoded).decode(), "width": int(panorama.shape[1]), "height": int(panorama.shape[0]), "processing_ms": round((time.perf_counter() - started) * 1000)}
