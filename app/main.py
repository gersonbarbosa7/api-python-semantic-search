from fastapi import FastAPI, Query
from pydantic import BaseModel
import numpy as np
from app.api.endpoints.search import router as seach_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Magazine - Assessment Test - ScottishPower by Gerson",
    description="Welcome to the Magazine Content Management API! This application provides a robust platform for managing and searching magazine content efficiently. With the integration of advanced features such as semantic search, the API enables users to retrieve and manipulate magazine information seamlessly. Desined by Gerson Barbosa - <a href='mailto:gersonbarbosa7@gmail.com'>gersonbarbosa7@gmail.com</a>"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a specific origin if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get('/', summary="To ensure that Application is running")
def welcome():
    return {"Welcome to the API hybrid by Gerson Barbosa"}

app.include_router(seach_router)