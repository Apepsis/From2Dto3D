# Product Requirements Document

## Problem

Creating a room tour usually needs specialist capture hardware or manual editing. Users need an accessible capture process and an honest signal when their photos are not sufficient for reconstruction.

## Primary user

A student, renter or small-property host who has a phone and wants to document a room.

## User journey

1. Create/select a room in the spatial graph.
2. Capture or upload 8–20 photos with 30–50% adjacent overlap.
3. Run analysis and correct blurry or weak-overlap frames.
4. Generate a panorama only when the evidence is sufficient.
5. Inspect the panorama and connect the room to the larger project graph.

## Acceptance criteria

- The client prevents a stitch request before a quality report says capture is ready.
- The API accepts 2–60 images, returns a per-frame sharpness and feature count, and reports adjacent match scores.
- A failed OpenCV stitch remains visible as a failure with retake guidance, never as a fabricated output.
- Room metadata persists locally and can contain an associated panorama.

## Non-goals in v0.1

Metric 3D mesh generation, automatic floorplans, semantic door detection, SLAM and neural rendering.
