import json
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import auth, crud, models, schemas
from .redis_client import get_redis_client
from .security import verify_password, create_access_token

app = FastAPI(title="Final API with Caching and Auth")

# --- Endpoints with Cache Invalidation ---

@app.post("/register", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(auth.get_db), redis_client = Depends(get_redis_client)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    redis_client.delete("all_users")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Protected and Cached Endpoints ---

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(db: Session = Depends(auth.get_db), redis_client = Depends(get_redis_client), admin_user: models.User = Depends(auth.require_admin)):
    cache_key = "all_users"
    cached_users = redis_client.get(cache_key)
    if cached_users:
        return json.loads(cached_users)

    users = crud.get_users(db)
    # Pydantic v2 requires this method for serialization from ORM objects
    users_serializable = [schemas.User.model_validate(user).model_dump() for user in users]
    
    redis_client.set(cache_key, json.dumps(users_serializable), ex=60)
    return users_serializable

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(auth.get_db), redis_client = Depends(get_redis_client), admin_user: models.User = Depends(auth.require_admin)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    redis_client.delete("all_users")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(auth.get_db), redis_client = Depends(get_redis_client), admin_user: models.User = Depends(auth.require_admin)):
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    redis_client.delete("all_users")
    return None