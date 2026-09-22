from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from CodePipeline!"}

@app.get("/test")
def read_test():
    return {"message": "The test route is working perfectly"}

# Mangum adapter for AWS Lambda
handler = Mangum(app)