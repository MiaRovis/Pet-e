import fastapi

app = fastapi.FastAPI()

@app.get("/")
async def proba():
        return "Okej"



