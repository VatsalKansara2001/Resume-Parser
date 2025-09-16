#!/bin/bash

# Resume Parser 2025 - Initialization Script
# This script sets up the complete development environment

set -e

echo "🚀 Initializing Resume Parser 2025..."

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads logs ml_models/trained_models

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec -T api alembic upgrade head || echo "⚠️  Migrations will run on first API start"

# Download ML models
echo "🧠 Setting up ML models..."
docker-compose exec -T api python -c "
import asyncio
from app.services.nlp_service import nlp_service
async def setup():
    await nlp_service.initialize()
    print('✅ NLP models loaded successfully')
asyncio.run(setup())
" || echo "⚠️  ML models will be downloaded on first use"

echo ""
echo "🎉 Resume Parser 2025 is ready!"
echo ""
echo "📍 Service URLs:"
echo "   • API Documentation: http://localhost:8000/docs"
echo "   • Grafana Dashboard: http://localhost:3001 (admin/admin)"
echo "   • Flower (Celery): http://localhost:5555"
echo "   • Frontend: http://localhost:3000"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop services: docker-compose down"
echo "   • Restart: docker-compose restart"
echo ""
echo "📖 Read the README.md for detailed documentation"
