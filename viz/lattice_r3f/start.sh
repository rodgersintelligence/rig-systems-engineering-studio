#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
[ -d "$DIR/node_modules" ] || (cd "$DIR" && npm install --no-audit --no-fund)
pgrep -f "vite.*lattice_r3f" > /dev/null || (cd "$DIR" && nohup npm run dev > /tmp/rig-lattice-r3f.log 2>&1 & disown)
sleep 2
open -a "Google Chrome" http://localhost:5173/
echo "lattice viewer: http://localhost:5173/"
