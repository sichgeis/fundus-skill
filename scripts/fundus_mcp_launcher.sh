#!/bin/sh
set -eu

case "$0" in
  */*) script_dir=${0%/*} ;;
  *) script_dir=. ;;
esac

if command -v python3 >/dev/null 2>&1; then
  exec python3 "$script_dir/fundus_mcp.py" "$@"
fi
if command -v python >/dev/null 2>&1; then
  exec python "$script_dir/fundus_mcp.py" "$@"
fi

echo "Fundus requires Python 3, but neither python3 nor python is available." >&2
exit 127
