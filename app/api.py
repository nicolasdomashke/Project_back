from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, PlainTextResponse
import sys
sys.path.append("..")
from database.bd import get_booking_info, add_booking, is_user_present, is_user_data_correct, add_user, is_event_present
import re

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

user_data_global = []

example = "Welcome to example route"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


def is_valid_email(email):
    pattern = r'^\w+@[a-zA-Z]+\.[a-zA-Z]+$'
    regex = re.compile(pattern)
    match = regex.fullmatch(email)
    return match is not None

def is_valid_password(password):
    pattern = r'^(?=.*\d)(?=.*[A-Z])[\w]{8,16}$'
    regex = re.compile(pattern)
    match = regex.fullmatch(password)
    return match is not None

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to the main page."}


@app.get("/reservation")
async def get_booking_table() -> dict:
    booking_table = get_booking_info()
    return {"data": booking_table}


@app.post("/reservation")
async def post_booking_table(new_user: dict):
    global user_data_global
    if not user_data_global:
        data = new_user["data"]
        data.append(user_data_global[0])
        if not is_event_present(data[0:2]):
            add_booking(data)


@app.post("/login")
async def post_login(user_data: dict):
    global user_data_global
    data = user_data['data']
    if is_user_present(data[0]):
        if is_user_data_correct(data):
            user_data_global = data
            RedirectResponse("/")
        else:
            RedirectResponse("/login")


@app.get("/login")
async def get_login():
    return {"data": "Login page"}


@app.post("/registration")
async def post_registration(user_data: dict):
    data = user_data['data']
    if is_user_present(data[1]):
        RedirectResponse("/registration")
        pass
    elif not is_valid_email(data[1]):
        RedirectResponse("/registration")
    elif not is_valid_password(data[2]):
        RedirectResponse("/registration")
    else:
        add_user(user_data)


@app.get("/registration")
async def get_registration():
    return {"data": "Registration page"}
