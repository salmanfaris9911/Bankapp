from fastapi import FastAPI
from routers import accounts


app = FastAPI(title="Banking API")


# Include the accounts router
app.include_router(accounts.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)