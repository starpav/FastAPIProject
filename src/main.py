import uvicorn
from fastapi import FastAPI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.routers.categories import router as categories_router
from src.routers.items import router as items_router


app = FastAPI()

app.include_router(categories_router)
app.include_router(items_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)