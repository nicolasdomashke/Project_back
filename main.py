import uvicorn
import sys
sys.path.append("..")
from database.bd import init_db

if __name__ == "__main__":
    with open("ipconfig.txt") as file:
        address = file.readline()
    init_db()
    uvicorn.run("app.api:app", host=address, port=8000, reload=True)