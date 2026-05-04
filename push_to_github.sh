#!/bin/bash

# Configuration
REPO_NAME="cpg-pricing-engine"
GITHUB_USER="rohankar02"

echo "Checking git status..."
git add .
git commit -m "Integrated standalone engine and analytics suite"

echo "To host on GitHub, run these commands:"
echo "1. gh repo create $REPO_NAME --public --source=. --remote=origin --push"
echo "   (Or if you don't have GitHub CLI:)"
echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "   git push -u origin main"
