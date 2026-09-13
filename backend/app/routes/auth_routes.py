import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from ..auth.security import verify_password, get_password_hash, create_access_token
from ..auth.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email.ilike(req.email)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )
        
    hashed_pwd = get_password_hash(req.password)
    new_user = User(
        full_name=req.full_name.strip(),
        company_name=req.company_name.strip(),
        email=req.email.lower().strip(),
        hashed_password=hashed_pwd,
        role=req.role or "Port Operator",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    token = create_access_token(
        data={"sub": new_user.email, "role": new_user.role, "name": new_user.full_name}
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "company_name": new_user.company_name,
            "email": new_user.email,
            "role": new_user.role
        }
    }

@router.post("/login", response_model=TokenResponse)
def login_user(req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email.ilike(req.email)).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
        
    expires = datetime.timedelta(days=30) if req.remember_me else datetime.timedelta(days=7)
    token = create_access_token(
        data={"sub": user.email, "role": user.role, "name": user.full_name},
        expires_delta=expires
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "company_name": user.company_name,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
