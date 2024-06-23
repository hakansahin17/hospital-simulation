import uvicorn
from app import app


if __name__ == "__main__":
    uvicorn.run(app, host="::", port=17217, log_level="info")
