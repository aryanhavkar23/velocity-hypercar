# Vehicle 3D assets - fill in after checking each model's Sketchfab page

| slug | model title | author | source URL | licence | notes |
|---|---|---|---|---|---|
| porsche-911-gt3-rs | | | https://sketchfab.com/3d-models/porsche-gt3-rs-e738eae819c34d19a31dd066c45e0f3d | | |
| suzuki-swift | | | https://sketchfab.com/3d-models/suzuki-swift-218c3c0c6afd4d0eb343bd50d8868fd0 | | |

Copy the author/licence line into `credit` of that car in `frontend/src/vehicleVisuals.js` to show it under the 3D view.
Only use models whose licence allows your use (CC-BY needs the credit; check "no commercial" licences for competitions).

## Adding another car
1. Put `<slug>.glb` in `assets/models/`.
2. Add the car (+ its engines / packages / aero) to `app/db/seed.py` and add an entry to `REGISTRY` in `frontend/src/vehicleVisuals.js`.
3. Restart the backend (it seeds on start). Cars not in `CARS` are deactivated automatically.

## If a model looks wrong
- Facing the wrong way: `model:{rotY:Math.PI}` in its registry entry.   - Too small/large in frame: `scale` / `camera`.
- Wrong part coloured (e.g. glass painted): run `npm run inspect`, then add `adapter:{body:[/regex/],glass:[/regex/],...}` or `ignore:[/regex/]`.
