# Coding Standards

- TypeScript runs in strict mode. No `any` in client-domain types.
- The API validates externally supplied images and gives actionable HTTP 422 errors.
- CV metrics must state their method and units. Do not label a heuristic as AI confidence.
- New processing stages must return failure states and latency in their response.
- Keep image bytes transient unless the user explicitly chooses storage.
- Add an experiment note whenever a capture/quality threshold changes.
- Run `npm run build` and `python -m py_compile api/app/main.py` before merging.
