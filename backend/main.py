from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .agent import agent, CodeFixRequest, CodeFixResponse

app = FastAPI(title="Architect Agent API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Architect Agent Backend is running"}

@app.post("/api/fix", response_model=CodeFixResponse)
async def fix_code(request: CodeFixRequest):
    try:
        result = await agent.fix_code(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
