import redis
from datetime import datetime
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.redis_url)

def check_budget(user_id: str, estimated_cost: float = 0.1):
    try:
        r.ping()
    except redis.exceptions.ConnectionError:
        return
        
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current = float(r.get(key) or 0)
    if current + estimated_cost > settings.monthly_budget_usd:
        raise HTTPException(status_code=402, detail="Monthly budget exceeded")
    
    r.incrbyfloat(key, estimated_cost)
    r.expire(key, 32 * 24 * 3600)
