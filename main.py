from fastapi import FastAPI
import requests
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "FastAPI proxy is running on Render"}

@app.get("/platforms")
def get_platforms(skip: int = 0, limit: int = 100):
    base_url = os.getenv(
        "DNAZ_BASE_URL",
        "https://dna-z-dev-web-api-backend.paas-bronze.astrazeneca.net"
    )
    url = f"{base_url}/platforms/?skip={skip}&limit={limit}"

    try:
        response = requests.get(
            url,
            headers={"accept": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        return {
            "status": "success",
            "count": len(data) if isinstance(data, list) else 1,
            "data": data[:5] if isinstance(data, list) else data
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "failure",
            "error": str(e),
            "url": url
        }
