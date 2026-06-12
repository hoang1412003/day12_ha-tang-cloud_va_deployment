import os
import signal
import logging
import json
import time
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import redis

from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.mock_llm import ask

logging.basicConfig(
    level=settings.log_level,
    format='{"time":"%(asctime)s","level":"%(levelname)s","msg":"%(message)s"}',
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
is_ready = False
r = redis.from_url(settings.redis_url)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global is_ready
    logger.info(json.dumps({"event": "startup", "port": settings.port}))
    is_ready = True
    yield
    is_ready = False
    logger.info("Shutting down gracefully...")
    time.sleep(0.1)

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "uptime": time.time() - START_TIME}

@app.get("/ready")
def ready():
    if not is_ready:
        return JSONResponse(status_code=503, content={"status": "not ready"})
    try:
        r.ping()
        return {"status": "ready"}
    except redis.exceptions.ConnectionError:
        return JSONResponse(status_code=503, content={"status": "redis not ready"})

@app.post("/ask")
def ask_question(
    request_data: dict,
    user_id: str = Depends(verify_api_key)
):
    question = request_data.get("question")
    if not question:
        raise HTTPException(status_code=422, detail="question required")
    
    # Manual dependency injection to handle parameters
    check_rate_limit(user_id)
    check_budget(user_id, 0.1)
    
    # Stateless history in Redis
    try:
        history_key = f"history:{user_id}"
        r.rpush(history_key, f"Q: {question}")
    except redis.exceptions.ConnectionError:
        pass
    
    logger.info(json.dumps({"event": "agent_request", "user": user_id}))
    response = ask(question)
    
    try:
        r.rpush(history_key, f"A: {response}")
    except redis.exceptions.ConnectionError:
        pass
        
    return {
        "question": question,
        "answer": response,
        "model": "mock-llm"
    }

def handle_sigterm(*args):
    logger.info("SIGTERM received")

signal.signal(signal.SIGTERM, handle_sigterm)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port)
