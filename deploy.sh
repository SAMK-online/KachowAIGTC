#!/bin/bash

# KachowAI - Google Cloud Run Deployment Script
# This script automates the deployment process

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       🚀 KachowAI - Google Cloud Run Deployment 🚀            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not found!${NC}"
    echo "Install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found!${NC}"
    echo "Install: https://docs.docker.com/get-docker/"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)

if [ -z "$PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  No project set${NC}"
    read -p "Enter your Google Cloud Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo -e "${GREEN}📦 Using project: ${PROJECT_ID}${NC}"
echo ""

# Prompt for API keys
read -sp "Enter your Gemini API Key: " GEMINI_KEY
echo ""
read -sp "Enter your ElevenLabs API Key (or press Enter to skip): " ELEVENLABS_KEY
echo ""
read -p "Enter your ElevenLabs Voice ID (or press Enter to skip): " VOICE_ID
echo ""

# Set region
REGION=${REGION:-us-central1}
SERVICE_NAME="kachowai"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔨 Building Docker image..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Build the image
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:latest .

echo -e "${GREEN}✅ Docker build complete${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "☁️  Pushing to Google Container Registry..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Configure Docker auth
gcloud auth configure-docker --quiet

# Push to GCR
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:latest

echo -e "${GREEN}✅ Image pushed to GCR${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Deploying to Cloud Run..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Build environment variables
ENV_VARS="GEMINI_API_KEY=${GEMINI_KEY},GEMINI_MODEL=gemini-2.5-flash-preview-09-2025"

if [ ! -z "$ELEVENLABS_KEY" ]; then
    ENV_VARS="${ENV_VARS},ELEVENLABS_API_KEY=${ELEVENLABS_KEY}"
fi

if [ ! -z "$VOICE_ID" ]; then
    ENV_VARS="${ENV_VARS},ELEVENLABS_VOICE_ID=${VOICE_ID}"
fi

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10 \
  --min-instances 0 \
  --set-env-vars "${ENV_VARS}"

# Get the URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}🎉 DEPLOYMENT SUCCESSFUL! 🎉${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${GREEN}✅ KachowAI is now live at:${NC}"
echo -e "${YELLOW}${SERVICE_URL}${NC}"
echo ""
echo "Next steps:"
echo "  1. Visit the URL above to test"
echo "  2. Share with users and get feedback"
echo "  3. Monitor logs: gcloud run services logs tail $SERVICE_NAME --region $REGION"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              Happy Voice Coding with KachowAI! 🎤             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
