# Deployment Information

## Public URL
https://your-agent-app.railway.app (Lưu ý: Thay link này bằng link thật sau khi deploy)

## Platform
Railway / Render

## Test Commands

### Health Check
```bash
curl https://your-agent-app.railway.app/health
# Expected: {"status": "ok", "uptime": ...}
```

### API Test (with authentication)
```bash
curl -X POST https://your-agent-app.railway.app/ask \
  -H "X-API-Key: my-secret-key" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

## Environment Variables Set
- PORT
- REDIS_URL
- AGENT_API_KEY
- LOG_LEVEL
- RATE_LIMIT_PER_MINUTE
- MONTHLY_BUDGET_USD

## Screenshots
- [Deployment dashboard](screenshots/dashboard.png)
- [Service running](screenshots/running.png)
- [Test results](screenshots/test.png)
