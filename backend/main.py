from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from backend.agent import agent, CodeFixRequest, CodeFixResponse

app = FastAPI(title="Architect Agent API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/fix", response_model=CodeFixResponse)
async def fix_code(request: CodeFixRequest):
    try:
        result = await agent.fix_code(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Serve Frontend (Must be last) ---
# Mount the React build directory (frontend/dist)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

    # Catch-all route to serve index.html for client-side routing
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # API requests are already handled above. This catches everything else.
        if full_path.startswith("api/"):
             raise HTTPException(status_code=404, detail="API endpoint not found")
        return FileResponse(os.path.join(frontend_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Backend running. Frontend build not found (run 'npm run build' in frontend/)."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
