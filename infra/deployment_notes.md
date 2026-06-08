# Deployment Notes

## Local

```bash
docker compose up -d postgres
make sample-panel
make sample-analysis
make dashboard
```

## Cloud

Recommended simple path:

1. Managed Postgres, such as Supabase or RDS.
2. Object storage for raw documents.
3. Streamlit deployment for dashboard.
4. GitHub Actions for lint/test.

## Secrets

Use environment variables or cloud secret manager. Never commit `.env`.
