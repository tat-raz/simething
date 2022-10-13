#from dataclasses import dataclass
from datetime import datetime
from http.client import HTTPException
from urllib import response
from xmlrpc.client import ResponseError
from fastapi import FastAPI, APIRouter, Path, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from pydantic_dataclasses import dataclass

app = FastAPI()

@app.get('/')
def ping():
    return 'pong'

@app.get(
    path='/hello',
    tags=['hello'],
    name='Печатай "Hello,world!"',
    description="Возвращает типовое приветсвие",
    )

#Функция, которая с нами здоровается

@app.get('/print')
def print_something(s:str=Query(default='трава', title='Строка поиска', min_lenght=5)):
    return{'msg':f'Печатаю что-то:{s}'}

@dataclass
class User:
    id:int
    username:str
    name:str
    last_name:str
    age:int
    created_at:datetime

#чтобы обновлять только часть данных
class UpdateUserSchema(BaseModel):
    id: Optional[int]
    username: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    age: Optional[int]
    created_at: Optional[datetime]


users = [
    User(id=1,username='andeq2',name='Andrew', last_name='Johns',age=23,created_at=datetime.now()),
    User(id=2,username='mar3',name='Marti',last_name='Fletcher',age=32,created_at=datetime.now()),
    User(id=3,username='bm69',name='Billy',last_name='Mirdack',age=45,created_at=datetime.now()),
]

#POST, GET, DELETE, PUT
#ВЫДЕЛИМ В ОТДЕЛЬНЫЙ РОУТЕР
#APIRouter - это изолированная часть нашего приложения

user_rourer = APIRouter(prefix='/users',tags=['Пользователи'])

#Схема наших возвращаемых данных
#class UserSchema(BaseModel):
#   id:int
#    username:str
#    name:str
#    last_name:str
#    age:int
#    created_at:datetime    
#
#    class Config:
#        schema_extra = {'example': {
#            'id':1,
#            'username':'john1',
#            'name':'John',
#            'last_name':'Doe',
#            'age':3,
#            'created_at':datetime.now(),
#        }
#        }


#Сделать метку пользователей более информативной
@dataclass
class UserList:
    count:int
    users:List[User]


#список всех пользователей
#response_model принимает некий тип данных,которые мы и возвращаем
@user_rourer.get('/', name='Все пользователи', response_model=UserList)
def get_all_users():
    return UserList(count=len(users), users=users)

#Возвращаем одного добавленого пользователя
@user_rourer.post('/', name='Добавить пользователя', response_model=User)
def create_user(user:User):
    users.append(user)
    return user

@user_rourer.get('/{user_id}', name='Получить пользователя', response_model=User)
def get_user(user_id:int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail='User not found')

#метод удаления
@user_rourer.delete('/{user_id}', name='Удалить пользователя', response_class=Response)
def delete_user(user_id: int):
    for i, user in enumerate(tuple(users)):
        if user.id == user_id:
            del users[i]
            break
    return Response(status_code=204)

#метод обновления
user_rourer.put('/{user_id}', name='Обновить данные пользователя', response_model=User)
def update_user(user_id: int, new_user_data: UpdateUserSchema):
    print(new_user_data.dict())
    for i in range(len(users)):
        if users[i].id == users_id:
            data = new_user_data.dict()
            for key in data:
                if data[key] is not None:
                    setattr(users[i], key, data[key])
        return users[i]
    raise HTTPException(status_code=404, detail='User not found')

#свяжем приложение с роутором с помощью include
@app.include_router(user_rourer)

