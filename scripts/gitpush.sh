#!/bin/bash

echo ""
echo "========== GIT STATUS =========="
git status
echo ""

echo "========== CHANGED FILES =========="
git diff --stat
echo ""

read -p "Commit message: " msg

if [ -z "$msg" ]; then
    echo "Commit message cannot be empty."
    exit 1
fi

tag="dev-$(date +%Y%m%d-%H%M%S)"

echo ""
echo "Using tag: $tag"
echo ""

git add .

git commit -m "$msg"

git tag "$tag"

echo ""
echo "Pushing to GitHub..."
echo ""

branch=$(git branch --show-current)

git push origin "$branch"
git push origin "$tag"

echo ""
echo "Done."
echo "Branch pushed: $branch"
echo "Tag created: $tag"
echo ""
