#!/usr/bin/env bash
# Capture representative generated CAD model pages in real headless Chrome.
#
# Usage:
#   capture_site_layout.sh <generated-site-dir> <scope>
#
# The generated Hugo site contains absolute URLs rooted at the public repository
# path. Mirror that path below a temporary localhost document root so the
# screenshots exercise the exact generated HTML/CSS/resource URLs before Pages
# publication.
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <generated-site-dir> <scope>" >&2
  exit 2
fi

site_dir="$1"
scope="$2"
repo_path="2026-011-02.cad.solidcraft"
visual_root="build/site-visual-root"
artifact_dir="artifacts/site-layout"
port="8765"

case "$scope" in
  main)
    public_path="$repo_path"
    ;;
  dev-cad|dev-ci)
    public_path="$repo_path/$scope"
    ;;
  *)
    echo "unsupported Pages scope for visual proof: $scope" >&2
    exit 2
    ;;
esac

test -d "$site_dir"
rm -rf "$visual_root" "$artifact_dir"
mkdir -p "$visual_root/$public_path" "$artifact_dir"
cp -a "$site_dir"/. "$visual_root/$public_path/"

python -m http.server "$port" \
  --bind 127.0.0.1 \
  --directory "$visual_root" \
  > "$artifact_dir/browser-server.log" 2>&1 &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null || true' EXIT

python - "$public_path" "$port" <<'PY'
import sys
import time
import urllib.request

public_path = sys.argv[1]
port = sys.argv[2]
url = f"http://127.0.0.1:{port}/{public_path}/models/plate/"
for _ in range(40):
    try:
        with urllib.request.urlopen(url, timeout=1) as response:
            if response.status == 200:
                break
    except Exception:
        time.sleep(0.25)
else:
    raise SystemExit("visual preview server did not become ready")
PY

chrome="$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || true)"
if [ -z "$chrome" ]; then
  echo "No Chrome/Chromium executable available on runner" >&2
  exit 1
fi

run_chrome() {
  local user_data_dir status
  user_data_dir="$(mktemp -d)"
  if timeout --signal=TERM --kill-after=5s 45s \
      "$chrome" \
      --user-data-dir="$user_data_dir" \
      --headless \
      --no-sandbox \
      --disable-gpu \
      --disable-dev-shm-usage \
      --hide-scrollbars \
      --virtual-time-budget=3500 \
      "$@"; then
    status=0
  else
    status=$?
  fi
  rm -rf "$user_data_dir"
  return "$status"
}

base="http://127.0.0.1:${port}/${public_path}"
plate_url="${base}/models/plate/"
simple_url="${base}/models/simple-mft/"

run_chrome \
  --window-size=1600,1400 \
  --screenshot="$PWD/$artifact_dir/plate-overview.png" \
  "$plate_url"

run_chrome \
  --window-size=1600,9000 \
  --screenshot="$PWD/$artifact_dir/plate-full.png" \
  "$plate_url"

run_chrome \
  --window-size=1600,1400 \
  --screenshot="$PWD/$artifact_dir/simple-mft-overview.png" \
  "$simple_url"

run_chrome \
  --window-size=1600,12000 \
  --screenshot="$PWD/$artifact_dir/simple-mft-full.png" \
  "$simple_url"

for image in \
  plate-overview.png \
  plate-full.png \
  simple-mft-overview.png \
  simple-mft-full.png; do
  test -s "$artifact_dir/$image"
done

if grep -Eq '"GET [^"]+" 404 ' "$artifact_dir/browser-server.log"; then
  echo "Rendered page requested one or more missing local assets:" >&2
  grep -E '"GET [^"]+" 404 ' "$artifact_dir/browser-server.log" >&2
  exit 1
fi
