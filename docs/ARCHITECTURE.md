# Architecture and extension map

## Current pipeline

```text
image capture → sharpness + ORB inspection → adjacent overlap → OpenCV stitcher
      ↓                                                             ↓
room graph in browser ← panorama + status + timing ← FastAPI response
```

## Replacement seams

| Current component | Upgrade path | Evidence required |
|---|---|---|
| ORB overlap heuristic | learned feature matcher (SuperPoint/LightGlue) | precision/recall on accepted captures |
| OpenCV stitcher | bundle adjustment + custom warping/blending | reprojection error and seam score |
| manually placed room nodes | pose graph / doorway detection | topology accuracy |
| wireframe room | monocular/multi-view depth or 3D Gaussian Splatting | geometry error and novel-view rating |

The current system intentionally keeps these seams explicit so a later research component can be evaluated against the baseline rather than just added as a label.
