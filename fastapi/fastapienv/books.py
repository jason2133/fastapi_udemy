from fastapi import FastAPI

app = FastAPI()

# RestFul API
# Asyncronous Function
# First Restful API using FastAPI
@app.get("/")
async def first_api():
    return {"message": "Hello Jason!"}

