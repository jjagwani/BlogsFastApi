# from fastapi import FastAPI
# from typing import Optional
# from pydantic import BaseModel

# app = FastAPI()


# @app.get('/blog')
# def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    
#     if published:
#         return {'data': f'{limit} published blogs from db'}
#     else:
#         return {'data': f'{limit} blogs from db'}

# @app.get('/blog/unpublished')
# def about():
#     return {'data': 'unpublished blogs'}

# @app.get('/blog/{id}')
# def about(id: int):
#     return {'data': id}

# @app.get('/blog/{id}/comments')
# def about(id: int):
#     return {'data': {'comments': id}}


# class Blog(BaseModel):
#     title: str
#     body: str
#     published: Optional[bool]


# @app.post('/blog')
# def createBlog(blog: Blog):
#     return {'data': f'Blog is created with title as {blog.title}'}