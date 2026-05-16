# RIG Lattice — R3F 3D Viewer

The public 3D viewer for the lattice. Built with Vite + React 18 + R3F (`@react-three/fiber`) + Three.js.

## Run locally

```bash
# From the repo root:
python3 -m lattice.generator
cp viz/lattice_index.json viz/lattice_r3f/public/lattice_index.json

# Then in this dir:
cd viz/lattice_r3f
npm install
npm run dev
# open http://localhost:5173
```

## Deploy to GitHub Pages

```bash
GITHUB_PAGES=true npm run build
# CI does this automatically — see .github/workflows/deploy-viz.yml
```

Live URL: https://rodgersintelligence.github.io/rig-systems-engineering-studio/

## Architecture

```
src/
  main.tsx                  # entry
  App.tsx                   # Canvas + UI panels
  components/
    Lattice.tsx             # InstancedMesh of all 3,087 cubes (one draw call)
    Axes.tsx                # 3D text labels via drei <Text>
    Sidebar.tsx             # Mode/altitude/diamond/confidence filters + BMS range
    CellPanel.tsx           # Right-side detail when a cell is clicked
    Legend.tsx              # Mode color legend (bottom-right)
  store/
    filters.ts              # zustand store for filter state
  lib/
    positions.ts            # cell → (x, y, z) grid mapping
  types/
    lattice.ts              # TypeScript types matching lattice_index.json
```

## Performance

- **1 draw call** for 3,087 cubes via `InstancedMesh`.
- Color + scale per-instance via `instanceMatrix` + `instanceColor` (typed arrays).
- Hover/click via `instanceId` from R3F's pointer event.
- Target: 60fps M1 Mac, 30fps mobile.

## Encoding

| Property | Encoding |
|---|---|
| Position | `(altitude_index, diamond_y_pos, confidence_z_pos)` in [0,6] × [0,20] × [0,20] |
| Color | Mode (green/yellow/orange/red per `MODE_COLORS`) |
| Scale | BMS, mapped linearly to edge length 0.2–0.9 |
| Opacity | Filtered cells dim to 0.08 alpha (kept visible for context) |

See [`docs/viz-design.md`](../../docs/viz-design.md) for the full multi-view design.
