#!/bin/bash
set -e

DIST_DIR="infra/lambda/dist"
OUT_DIR="build/lambda"
ZIP_PATH="$OUT_DIR/lambda.zip"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$OUT_DIR"

pip install -r requirements.txt -t "$DIST_DIR"

cp -r src/* "$DIST_DIR/"

cd "$DIST_DIR"
zip -r "../../$(basename "$OUT_DIR")/lambda.zip" .
