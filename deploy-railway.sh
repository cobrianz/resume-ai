#!/bin/bash

# Quick Railway Deployment Setup Script

echo "Resume AI - Railway Deployment Setup"
echo "===================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
fi

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "Enter your GitHub repository URL (e.g., https://github.com/username/resume-ai.git):"
    read REPO_URL
    git remote add origin $REPO_URL
fi

echo "Adding files..."
git add .

echo "Creating initial commit..."
git commit -m "Initial commit: Resume AI application ready for Railway"

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "=========================================="
echo "Next steps:"
echo "=========================================="
echo ""
echo "1. Go to https://railway.app"
echo "2. Click 'New Project' → 'Deploy from GitHub repo'"
echo "3. Select your 'resume-ai' repository"
echo "4. Click 'Deploy Now'"
echo ""
echo "5. Once deployed, go to Variables tab and add:"
echo "   OPENAI_API_KEY=sk-your-actual-key"
echo "   PROJECT_NAME=Resume AI"
echo "   API_V1_STR=/api/v1"
echo "   MAX_UPLOAD_SIZE=10485760"
echo ""
echo "6. Railway will auto-deploy and provide your URL"
echo ""
echo "Done! Your app will be live in a few minutes."
