from fastapi import FastAPI

app = FastAPI()
# Comienzo a montar el servidor


@app.get('/')
async def root():
    return {'message': 'Hello World!!'}
