from datetime import datetime, time, timedelta
from typing import Optional, List, Set, Dict, Union
from uuid import UUID

from fastapi import FastAPI, Query, Path, Body, Cookie, Header, status, Form, File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, EmailStr

app = FastAPI()


# # 기본 api(dict, list, str, int 뿐만 아니라 지정한 형식(뒤에서 나옴)으로 return 해줄 수 있음)
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# # 경로로 파라미터 받기, 타입 지정
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}
#
#
# # 순서 신경쓰기
# @app.get("/users/me")
# async def read_user_me():
#     return {"user_id": "the current user"}
#
#
# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id": user_id}
#
#
# # 정해둔 옵션만 선택할 수 있도록 하는 방법
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"
#
#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name == ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#
#     return {"model_name": model_name, "message": "Have some residuals"}
#
#
# # 경로 자체를 파라미터로 받을 경우
# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}
#
#
# # 경로 파라미터가 아닌 경우엔 쿼리 파라미터로 인식함
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
#
#
# # Optional 파라미터 지정하기
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None):
#     if q:
#         return {"item_id": item_id, "q": q}
#     return {"item_id": item_id}
#
#
# # bool 타입 파라미터
# @app.get("/items/{item_id}")
# async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
#
#
# # 여러개의 경로 파라미터와 쿼리 파라미터를 동시에 사용할 수 있고, 알아서 적절하게 분류해서 받아줌
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
#
#
# # 쿼리 파라미터를 무조건 받아야한다면 Optional이나 default 값을 주지 않으면 됨
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str):
#     item = {"item_id": item_id, "needy": needy}
#     return item
#
#
# @app.get("/items/{item_id}")
# async def read_user_item(item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None):
#     item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
#     return item
#
#
# # Pydantic을 사용해서 request body 받기
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#
#
# @app.post("/items/")
# async def create_item(item: Item):
#     return item
#
#
# # model 사용할 수 있음
# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict
#
#
# # Request body + path + query parameters 모두 사용할 수 있음
# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item, q: Optional[str] = None):
#     result = {"item_id": item_id, **item.dict()}
#     if q:
#         result.update({"q": q})
#     return result
#
#
# # 추가적인 조건을 더 줄 수 있음
# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(None, max_length=50)):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # Query parameter list / multiple values¶
# @app.get("/items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     query_items = {"q": q}
#     return query_items
#
#
# # list를 사용해서 할 수도 있는데, 이 경우에는 list 내의 요소들의 타입까지는 체크하지 않음
# @app.get("/items/")
# async def read_items(q: list = Query([])):
#     query_items = {"q": q}
#     return query_items
#
#
# # 쿼리 파라미터의 이름이 유효하지 않지만 무조건 사용해야하는 경우
# @app.get("/items/")
# async def read_items(q: Optional[str] = Query(None, alias="item-query")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # 사용하지 않는 것으로 표현하기
# @app.get("/items/")
# async def read_items(
#     q: Optional[str] = Query(
#         None,
#         alias="item-query",
#         title="Query string",
#         description="Query string for the items to search in the database that have a good match",
#         min_length=3,
#         max_length=50,
#         regex="^fixedquery$",
#         deprecated=True,
#     )
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # 경로 파라미터에서도 여러가지 처리를 해줄 수 있음
# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: int = Path(..., title="The ID of the item to get"),
#     q: Optional[str] = Query(None, alias="item-query"),
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # 숫자 벨리데이션
# @app.get("/items/{item_id}")
# async def read_items(
#     *,
#     item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
#     q: str,
#     size: float = Query(..., gt=0, lt=10.5)
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # body 파라미터 여러개 받기
# class User(BaseModel):
#     username: str
#     full_name: Optional[str] = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, user: User):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results
#
#
# # Body도 Path, Query 처럼 여러가지 조건을 달아줄 수 있음
# @app.put("/itemssss/{item_id}")
# async def updatesss_item(
#     *,
#     item_id: int,
#     item: Item,
#     user: User,
#     importance: int = Body(..., gt=0),
#     q: Optional[str] = None
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     if q:
#         results.update({"q": q})
#     return results
#
#
# # 원래 하나의 item을 요청에 보낸다고 하면,
# # {
# #     "name": "Foo",
# #     "description": "The pretender",
# #     "price": 42.0,
# #     "tax": 3.2
# # }
# # 이런식인데
# # embed를 true로 설정하면
# # {
# #     "item": {
# #         "name": "Foo",
# #         "description": "The pretender",
# #         "price": 42.0,
# #         "tax": 3.2
# #     }
# # }
# # 이런식으로 key값을 따로 줄 수 있음
# @app.put("/itemseeeee/{item_id}")
# async def updateeee_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results


# # Pydantic의 Field를 써서 validation과 metadata를 선언해줄 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = Field(
#         None, title="The description of the item", max_length=300
#     )
#     price: float = Field(..., gt=0, description="The price must be greater than zero")
#     tax: Optional[float] = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results


# # 내부의 데이터 타입에 list를 사용할 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: list = []
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# # 이렇게 List[]를 사용하면 내부의 타입까지 지정해줄 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: List[str] = []
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# # Set 타입도 사용할 수 있음, 중복값이 들어가 있으면 하나씩만 받아옴
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = set()
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# # 중첩 모델을 사용해서 타입으로 지정할 수 있음
# class Image(BaseModel):
#     url: str
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#     image: Optional[Image] = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results


# # pydantic에서 여러가지 타입들을 지원해줌
# # https://pydantic-docs.helpmanual.io/usage/types/
# class Image(BaseModel):
#     url: HttpUrl
#     name: str
#
#
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = set()
#     image: Optional[Image] = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# # 딕셔너리도 사용할 수 있음
# @app.post("/index-weights/")
# async def create_index_weights(weights: Dict[int, float]):
#     return weights

# # swagger에 보여질 예시를 작성해줄 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# # 필드에 직접 예시를 줄 수도 있음
# class Item(BaseModel):
#     name: str = Field(..., example="Foo")
#     description: Optional[str] = Field(None, example="A very nice Item")
#     price: float = Field(..., example=35.4)
#     tax: Optional[float] = Field(None, example=3.2)
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# # body에서 줄 수도 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int,
#     item: Item = Body(
#         ...,
#         example={
#             "name": "Foo",
#             "description": "A very nice Item",
#             "price": 35.4,
#             "tax": 3.2,
#         },
#     ),
# ):
#     results = {"item_id": item_id, "item": item}
#     return results


# # 다양한 타입을 사용할 수 있음
# @app.put("/items/{item_id}")
# async def read_items(
#     item_id: UUID,
#     start_datetime: Optional[datetime] = Body(None),
#     end_datetime: Optional[datetime] = Body(None),
#     repeat_at: Optional[time] = Body(None),
#     process_after: Optional[timedelta] = Body(None),
# ):
#     start_process = start_datetime + process_after
#     duration = end_datetime - start_process
#     return {
#         "item_id": item_id,
#         "start_datetime": start_datetime,
#         "end_datetime": end_datetime,
#         "repeat_at": repeat_at,
#         "process_after": process_after,
#         "start_process": start_process,
#         "duration": duration,
#     }

# # 쿠키 사용
# @app.get("/items/")
# async def read_items(ads_id: Optional[str] = Cookie(None)):
#     return {"ads_id": ads_id}

# # 헤더 사용
# @app.get("/items/")
# async def read_items(user_agent: Optional[str] = Header(None)):
#     return {"User-Agent": user_agent}


# # 응답할 때도 model을 사용할 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: List[str] = []
#
#
# @app.post("/items/", response_model=Item)
# async def create_item(item: Item):
#     return item

# # 주의해야할 점! input과 output모델을 따로 만들어야함, 패스워드가 노출될 수 있음
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user: UserIn):
#     return user

# # 응답 모델에 dafault를 줄 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: float = 10.5
#     tags: List[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
# async def read_item(item_id: str):
#     return items[item_id]

# # 포함하거나 안할 필드를 선택할 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: float = 10.5
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
#     "baz": {
#         "name": "Baz",
#         "description": "There goes my baz",
#         "price": 50.2,
#         "tax": 10.5,
#     },
# }
#
#
# @app.get(
#     "/items/{item_id}/name",
#     response_model=Item,
#     response_model_include={"name", "description"},
# )
# async def read_item_name(item_id: str):
#     return items[item_id]
#
#
# @app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
# async def read_item_public_data(item_id: str):
#     return items[item_id]


# # 모델을 여러개 사용해야함
# # input용, output용, db저장용 모델을 만들어서 사용함
# class UserIn(BaseModel):
#     username: str
#     password: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserOut(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserInDB(BaseModel):
#     username: str
#     hashed_password: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password
#
#
# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved


# # 중복을 피하기 위해서 상속해서 쓰는 방법이 있음(주로 이런식으로 코드를 짤거같음, 파일만 나눠서)
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: Optional[str] = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# class UserInDB(UserBase):
#     hashed_password: str
#
#
# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password
#
#
# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

# # 응답 모델에 Union을 써서 여러개중에 하나의 타입으로 응답하도록 할 수 있음
# class BaseItem(BaseModel):
#     description: str
#     type: str
#
#
# class CarItem(BaseItem):
#     type = "car"
#
#
# class PlaneItem(BaseItem):
#     type = "plane"
#     size: int
#
#
# items = {
#     "item1": {"description": "All my friends drive a low rider", "type": "car"},
#     "item2": {
#         "description": "Music is my aeroplane, it's my aeroplane",
#         "type": "plane",
#         "size": 5,
#     },
# }
#
#
# @app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
# async def read_item(item_id: str):
#     return items[item_id]


# # list 형태로 응답할 수도 있음
# class Item(BaseModel):
#     name: str
#     description: str
#
#
# items = [
#     {"name": "Foo", "description": "There comes my hero"},
#     {"name": "Red", "description": "It's my aeroplane"},
# ]
#
#
# @app.get("/items/", response_model=List[Item])
# async def read_items():
#     return items


# # 딕셔너리 타입으로 응답
# @app.get("/keyword-weights/", response_model=Dict[str, float])
# async def read_keyword_weights():
#     return {"foo": 2.3, "bar": 3.4}


# # status 코드
# @app.post("/items/", status_code=status.HTTP_201_CREATED)
# async def create_item(name: str):
#     return {"name": name}


# # json이 아니라 form으로 받을 경우
# @app.post("/login/")
# async def login(username: str = Form(...), password: str = Form(...)):
#     return {"username": username}


# # 파일 업로드
# # File 사용
# @app.post("/files/")
# async def create_file(file: bytes = File(...)):
#     return {"file_size": len(file)}
#
# # UploadFile 사용
# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File(...)):
#     return {"filename": file.filename}

# # 파일 업로드 여러개
# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}
#
#
# @app.post("/uploadfiles/")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     return {"filenames": [file.filename for file in files]}
#
#
# @app.get("/")
# async def main():
#     content = """
# <body>
# <form action="/files/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
# <input name="files" type="file" multiple>
# <input type="submit">
# </form>
# </body>
#     """
#     return HTMLResponse(content=content)


# # 여러개 한 번에 받기(form으로)
# @app.post("/files/")
# async def create_file(
#     file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }


## 에러에 대한 응답
# items = {"foo": "The Foo Wrestlers"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"item": items[item_id]}

# # 헤더 추가
# items = {"foo": "The Foo Wrestlers"}
#
#
# @app.get("/items-header/{item_id}")
# async def read_item_header(item_id: str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail="Item not found",
#             headers={"X-Error": "There goes my error"},
#         )
#     return {"item": items[item_id]}


# 에러메시지를 커스텀하는 여러가지 방법들이 존재함
# 나중에 필요하면 해당 링크의 하단 부분을 참고하자
# https://fastapi.tiangolo.com/ko/tutorial/handling-errors/


# # tags 쓰는 법
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
#
# @app.post("/items/", response_model=Item, tags=["items"])
# async def create_item(item: Item):
#     return item
#
#
# @app.get("/items/", tags=["items"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]
#
#
# @app.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "johndoe"}]


# 요약과 설명 달기
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
#
# @app.post(
#     "/items/",
#     response_model=Item,
#     summary="Create an item",
#     description="Create an item with all the information, name, description, price, tax and a set of unique tags",
# )
# async def create_item(item: Item):
#     return item

# # docstring으로 설명을 적을 수 있음
# # markdown 쓰는 방식과 똑같음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
#
# @app.post("/items/", response_model=Item, summary="Create an item")
# async def create_item(item: Item):
#     """
#     Create an item with all the information:
#
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item

# # 응답에도 설명을 달 수 있음
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = []
#
#
# @app.post(
#     "/items/",
#     response_model=Item,
#     summary="Create an item",
#     response_description="The created item",
# )
# async def create_item(item: Item):
#     """
#     Create an item with all the information:
#
#     - **name**: each item must have a name
#     - **description**: a long description
#     - **price**: required
#     - **tax**: if the item doesn't have tax, you can omit this
#     - **tags**: a set of unique tag strings for this item
#     """
#     return item


# # 사용안하는 api 표시해주기
# @app.get("/items/", tags=["items"])
# async def read_items():
#     return [{"name": "Foo", "price": 42}]
#
#
# @app.get("/users/", tags=["users"])
# async def read_users():
#     return [{"username": "johndoe"}]
#
#
# @app.get("/elements/", tags=["items"], deprecated=True)
# async def read_elements():
#     return [{"item_id": "Foo"}]

# # 데이터를 JSON과 호환되도록 맞춰줘야할 때가 있음
# # jsonable_encoder 사용
# fake_db = {}
#
#
# class Item(BaseModel):
#     title: str
#     timestamp: datetime
#     description: Optional[str] = None
#
#
# app = FastAPI()
#
#
# @app.put("/items/{id}")
# def update_item(id: str, item: Item):
#     json_compatible_item_data = jsonable_encoder(item)
#     fake_db[id] = json_compatible_item_data


# 객체 데이터를 update할 때, 객체 전체를 업데이트하면 PUT, 일부만 업데이트할 때는 PATCH를 사용하는게 원칙
# 강제적인 것은 아님

# # 하지만 다음처럼 일부만 수정하는데 PUT을 사용하면 갱신하지 않으려던 데이터까지 갱신될 수 있으니 조심해야함
# class Item(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     tax: float = 10.5
#     tags: List[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]
#
#
# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded

# # 일부만 수정하려면 다음과 같은 과정으로해야함
# class Item(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     tax: float = 10.5
#     tags: List[str] = []
#
#
# items = {
#     "foo": {"name": "Foo", "price": 50.2},
#     "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
#     "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
# }
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: str):
#     return items[item_id]
#
#
# @app.patch("/items/{item_id}", response_model=Item)
# async def update_item(item_id: str, item: Item):
#     stored_item_data = items[item_id]
#     stored_item_model = Item(**stored_item_data)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     return updated_item
