web: cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT}
frontend: cd frontend && npm install && npm run build && npx serve -s dist -l ${FRONTEND_PORT:-5173}
