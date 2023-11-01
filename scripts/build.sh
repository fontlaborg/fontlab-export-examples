#!/usr/bin/env bash
dir=${0%/*}
if [ "$dir" = "$0" ]; then dir="."; fi
cd "$dir"
CONFIG="./fontlab_build.yaml"
"/Applications/FontLab 8.app/Contents/MacOS/FontLab 8" ./fontlab_export.vfpy "$CONFIG"
echo "If FontLab does not quit automatically after export, quit it manually."
