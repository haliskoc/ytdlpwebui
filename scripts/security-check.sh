#!/bin/bash

# Security Check Script for yt-dlp Web UI
# This script performs security checks before deployment

echo "🔒 Running Security Checks..."

# Check for sensitive files
echo "📁 Checking for sensitive files..."
if [ -f ".env" ]; then
    echo "❌ ERROR: .env file found! Remove before committing."
    exit 1
fi

if [ -d "venv" ] || [ -d "backend/venv" ]; then
    echo "❌ ERROR: Virtual environment found! Remove before committing."
    exit 1
fi

if [ -d "node_modules" ] || [ -d "frontend/node_modules" ]; then
    echo "❌ ERROR: node_modules found! Remove before committing."
    exit 1
fi

# Check for hardcoded secrets
echo "🔍 Checking for hardcoded secrets..."
if grep -r "password.*=.*[\"'][^\"']*[\"']\|secret.*=.*[\"'][^\"']*[\"']\|api_key.*=.*[\"'][^\"']*[\"']\|token.*=.*[\"'][^\"']*[\"']" . --include="*.py" --include="*.js" --include="*.jsx" | grep -v "package-lock.json" | grep -v "test" | grep -v "example" | grep -v "template"; then
    echo "❌ ERROR: Potential hardcoded secrets found!"
    exit 1
fi

# Check for personal information
echo "👤 Checking for personal information..."
if grep -r "/home/\|/tmp/ytdlp\|lenovo" . --include="*.py" --include="*.js" --include="*.jsx" --include="*.md" | grep -v "localhost" | grep -v "127.0.0.1"; then
    echo "❌ ERROR: Personal information found!"
    exit 1
fi

# Check for dangerous functions
echo "⚠️  Checking for dangerous functions..."
if grep -r "os\.system\|eval\s*\(\|exec\s*\(" . --include="*.py" | grep -v "subprocess_exec" | grep -v "test" | grep -v "retrieval"; then
    echo "❌ ERROR: Dangerous functions found!"
    exit 1
fi

# Check .gitignore
echo "📋 Checking .gitignore..."
if [ ! -f ".gitignore" ]; then
    echo "❌ ERROR: .gitignore file missing!"
    exit 1
fi

# Check for required security files
echo "📄 Checking security documentation..."
required_files=("SECURITY.md" "CONTRIBUTING.md" "DEPLOYMENT.md")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ERROR: $file missing!"
        exit 1
    fi
done

echo "✅ All security checks passed!"
echo "🚀 Project is ready for GitHub upload!"
