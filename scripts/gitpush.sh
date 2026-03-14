#!/bin/bash

# Git helper script with dynamic timestamp tags

echo ""
echo "Current git status:"
git status
echo ""

read -p "Commit message: " msg

if [ -z "$msg" ]; then
    echo "Commit message cannot be empty."
    exit 1
fi

# Generate timestamp tag
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

git push origin $(git branch --show-current)

git push origin "$tag"

echo ""
echo "Done."
echo "Tag created: $tag"
echo ""

