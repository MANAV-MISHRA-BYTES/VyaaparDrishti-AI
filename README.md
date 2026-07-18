# VyaaparDrishti AI 

Bringing invisible rural micro-enterprises into formal credit networks using AI-driven document extraction and alternative data synthesis. Built for the NABARD Hackathon @ GFF 2026.

## Overview
Over 80% of rural micro-enterprises are "credit-blind," managing cash flow via unstructured paper ledgers (Bahi-Khatas). VyaaparDrishti AI is a lightweight cognitive intelligence platform that digitizes physical notes instantly via a smartphone camera, fusing this newly structured data with localized digital payment signals to construct a high-fidelity dynamic cash flow profile and risk score.

## Architecture & Tech Stack
* **Frontend:** Vue.js (Lightweight, optimized for low-bandwidth environments)
* **Backend Gateway:** Python / Flask
* **Asynchronous Processing:** Celery task routing + Redis message broker
* **Database:** MongoDB for unstructured ledger telemetry
* **Deployment:** Vercel (Client) & Render (Services)

## Repository Structure
* `/frontend` - Vue.js application codebase
* `/backend` - Flask API and Celery worker configurations

## Local Execution
Ensure Docker is installed for localized database mocking.

1. Start Redis and MongoDB:
   docker run -d -p 6379:6379 redis:alpine
   docker run -d -p 27017:27017 mongo:latest

2. Start the Celery Worker (inside `/backend`):
   celery -A app.celery worker --loglevel=info

3. Start the Flask API (inside `/backend`):
   python app.py

4. Serve the Frontend (inside `/frontend`):
   npm run serve
