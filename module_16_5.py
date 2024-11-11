from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory='templates')

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int


@app.get('/user/{user_id}')
async def get_(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, 'user': users[user_id-1]})


@app.post('/user/{username}/{age}')
async def post_(user: User) -> str:
    if len(users) == 0:
        user.id = 1
    else:
        last_user = users[-1]
        user.id = last_user.id+1
    users.append(user)
    return f'User {user.id} is registered'


@app.put('/user/{user_id}/{username}/{age}')
async def put_(user_id: int, user: User) -> str:
    try:
        edit_user = users[user_id-1]
        edit_user.username = user.username
        edit_user.age = user.age
        print(f'The user {user_id} has been updated')
        return edit_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.delete('/user/{user_id}')
async def delete_(user_id: int) -> str:
    try:
        delete_user = users[user_id-1]
        users.remove(delete_user)
        print(f'User {user_id} has been deleted')
        return delete_user
    except IndexError:
        raise HTTPException(status_code=404, detail='User was not found')


@app.get('/')
async def get_(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {"request": request, 'users': users})
