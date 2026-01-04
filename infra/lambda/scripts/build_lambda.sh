#!/bin/bash
set -e
DIST_DIR="infra/lambda/dist"
OUT_DIR="build/lambda"
ZIP_PATH="$OUT_DIR/lambda.zip"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
pip install -r requirements.txt -t "$DIST_DIR"
cp -r src/* "$DIST_DIR/"
if [ -f "$ZIP_PATH" ]; then
    rm "$ZIP_PATH"
fi
mkdir -p "$OUT_DIR"
cd "$DIST_DIR"
zip -r "$PWD/../../../$ZIP_PATH" .
ls -lh "$PWD/../../../$ZIP_PATH"
