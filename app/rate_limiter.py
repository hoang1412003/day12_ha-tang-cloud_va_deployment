import redis
import time
from fastapi import HTTPException
from .config import settings

r = redis.from_url(settings.redis_url)

def check_rate_limit(user_id: str):
    """Rate limit: Sliding window using Redis."""
    try:
        r.ping() # test conn
    except redis.exceptions.ConnectionError:
        return # Skip if redis is not available during simple local test without redis
        
    current_time = time.time()
    window_start = current_time - 60
    key = f"rate_limit:{user_id}"

    # Remove old requests
    r.zremrangebyscore(key, 0, window_start)
    
    # Count requests in window
    request_count = r.zcard(key)
    
    if request_count >= settings.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
    # Add current request
    r.zadd(key, {str(current_time): current_time})
    r.expire(key, 60)
