# Final Production-Ready AI Agent

## Features
- Multi-stage Docker build
- Fast API application
- Redis integration for stateless persistence, rate limiting, and cost guard
- API Key Authentication
- Health and Readiness Probes

## Setup

1. Copy environment variables
```bash
cp .env.example .env
```
2. Adjust environment variables inside `.env` if necessary.

## Running locally

Using docker-compose:
```bash
docker compose up --build
```
This will start the Redis server, 1 agent container, and Nginx at port 80.
You can scale the agent:
```bash
docker compose up --build --scale agent=3
```

## Testing endpoints
Health check:
```bash
curl http://localhost/health
```
Chat endpoint:
```bash
curl -X POST http://localhost/ask -H "X-API-Key: my-secret-key" -H "Content-Type: application/json" -d '{"question": "Hello!"}'
```
