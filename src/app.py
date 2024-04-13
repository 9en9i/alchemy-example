from fastapi import FastAPI

from src.books.views import router as book_router

app = FastAPI()

app.include_router(book_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
    )
