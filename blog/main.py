from contextlib import asynccontextmanager
import copy
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import async_session, init_db, engine
from .models import Blog
from .schemas import BlogRequest, BlogResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

async def get_db():
    async with async_session() as session:
        yield session

@app.post("/blog", status_code=status.HTTP_201_CREATED, response_model=BlogResponse)
async def create_blog(request: BlogRequest, db: AsyncSession = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=List[BlogResponse])
async def get_all_blogs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog))
    blogs = result.scalars().all()
    return blogs

@app.get("/blog/{id}", response_model=BlogResponse)
async def get_blog(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == id))
    blog = result.scalars().first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == id))
    blog = result.scalars().first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Blog with id {id} is not available")
    
    await db.delete(blog)
    await db.commit()
    return

@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=BlogResponse)
async def update_blog(id: int, request: BlogRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Blog).where(Blog.id == id))
    blog = result.scalars().first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Blog with id {id} is not available")
    
    blog.title = request.title
    blog.body = request.body
    await db.commit()
    await db.refresh(blog)
    return blog
    
