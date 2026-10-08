import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from fastapi import HTTPException, status

from app.models import User
from app.schemas.auth import UserRegisterRequest, UserLoginRequest, TokenResponse, UserResponse
from app.core.security import hash_password, verify_password, create_access_token

logger = logging.getLogger("enterprise_rag")


class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, request: UserRegisterRequest) -> UserResponse:
        """
        Registers a new user account with transaction rollback & error handling.
        """
        # 1. Duplicate email check
        try:
            result = await db.execute(select(User).where(User.email == request.email.lower()))
            existing_user = result.scalars().first()
        except (SQLAlchemyError, DBAPIError) as e:
            logger.error(f"Database error during registration lookup: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service is temporarily unavailable."
            )

        if existing_user:
            logger.info(f"Registration conflict: duplicate email '{request.email.lower()}'")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists."
            )

        # 2. Hash password & add user
        hashed_pwd = hash_password(request.password)
        new_user = User(
            email=request.email.lower(),
            hashed_password=hashed_pwd,
            full_name=request.full_name
        )

        # 3. Transaction Commit with Rollback
        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            logger.info(f"User registration successful for email '{new_user.email}'")
            return UserResponse.model_validate(new_user)
        except (SQLAlchemyError, DBAPIError) as e:
            await db.rollback()
            logger.error(f"Database commit failure during user registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service is temporarily unavailable."
            )
        except Exception as e:
            await db.rollback()
            logger.error(f"Unexpected error during user registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected server error occurred."
            )

    @staticmethod
    async def login_user(db: AsyncSession, request: UserLoginRequest) -> TokenResponse:
        try:
            result = await db.execute(select(User).where(User.email == request.email.lower()))
            user = result.scalars().first()
        except (SQLAlchemyError, DBAPIError) as e:
            logger.error(f"Database error during login lookup: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service is temporarily unavailable."
            )

        if not user or not verify_password(request.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = create_access_token(user.id)
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserResponse.model_validate(user)
        )
