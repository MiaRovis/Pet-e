import fastapi

app = fastapi

@app.get("/")
async def proba():
        return "Okej"



