from fastapi import FastAPI

app = FastAPI()

@app.post("/hash/")
def hash_text(text: str):
    print(text)
    try:
        result = "this was your text : " + text
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}

