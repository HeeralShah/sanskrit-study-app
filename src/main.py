from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/health")
def health_check() :
    return "OK", 200


handler = Mangum(app)