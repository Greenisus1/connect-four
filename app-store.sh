#!/bin/bash
# pi-app-store: 1
# pi-app-store-category: games
# pi-app-store-description: Terminal four-in-a-row, two local players or simple computer.
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-}" in
 install) python3 -c 'from pathlib import Path;compile(Path("connect_four.py").read_bytes(), "connect_four.py", "exec")' ;;
 run) shift; exec python3 connect_four.py "$@" ;;
 *) echo 'Use: bash app-store.sh install OR bash app-store.sh run';exit 1 ;;
esac
