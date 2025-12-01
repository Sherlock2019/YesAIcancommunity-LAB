#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Checking for files bigger than 95MB..."
BIGFILES=$(find . -type f -size +95M)

if [[ -n "$BIGFILES" ]]; then
    echo "❌ ERROR: The following files exceed GitHub's 100MB limit:"
    echo "$BIGFILES"
    echo "👉 Fix: compress/delete or add to Git LFS before pushing."
    exit 1
fi

echo "📦 Adding all files..."
git add -A

echo "📝 Committing..."
git commit -m "Safe push" || true

echo "🚀 Pushing to GitHub..."
git push -u origin main
