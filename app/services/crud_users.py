from typing import Any, Dict, Optional, Union
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from .base import CRUDBase
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.core.security import settings
from app.utils import is_password_complex

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # CREATE

    def create(self, db: Session, user: UserCreate) -> User:
        is_complex, criteria_not_accomplish = is_password_complex(user.password_hash)
        if not is_complex:
            message = f"La contraseña no cumple con los siguientes criterios: {', '.join(criteria_not_accomplish)}"
            raise HTTPException(status_code=400, detail=message)
        else:
            db_obj = User(
                fullname=user.fullname,
                username = user.username,
                email=user.email,
                password_hash=get_password_hash(user.password_hash),
                is_authenticated=user.is_authenticated,
                is_superuser=user.is_superuser,
                is_blocked=user.is_blocked
            )
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
    # READ
    def get_by_id(self, db: Session, id: int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    # UPDATES

    def _update_password(self, db: Session, user: User, confirm_password: str, new_password: str) -> User:
        # validate
        if confirm_password != new_password:
            raise HTTPException(
               status_code=400, detail="Las contraseñas no coinciden")
        
        is_complex, criteria_not_accomplish = is_password_complex(new_password)
        if not is_complex:
            message = f"La contraseña no cumple con los siguientes criterios: {', '.join(criteria_not_accomplish)}"
            raise HTTPException(status_code=400, detail=message)

        # update
        user_update = UserUpdate(password_hash=get_password_hash(new_password))
        return super().update(db,db_obj=user,obj_in=user_update)

    def _unlock_account(self, db: Session, user: User):
        userUpdate = UserUpdate(is_blocked=False, attempts_login_failed=0)
        return super().update(db,db_obj=user,obj_in=userUpdate)
    
    # AUTHENTICATE
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        # get user
        user = self.get_by_email(db, email=email)
        # validate user
        if not user:
            raise HTTPException(
                status_code=400, detail="Email incorrecto.")
    
        if user.attempts_login_failed == 3:
            raise HTTPException(
                status_code=400, detail=f"Su cuenta está bloqueada, por favor ponerse en contacto con el administrador.")
        
        if user and not verify_password(password, user.password_hash):
            if user.attempts_login_failed == 3:
                user.is_blocked = True
                user_update = UserUpdate(is_blocked=user.is_blocked)
                super().update(db,db_obj=user,obj_in=user_update)
                raise HTTPException(
                status_code=400, detail=f"Se ha bloqueado la cuenta, para el usuario {user.username}, por favor ponerse en contacto con el administrador.")
            else:
                user.attempts_login_failed = user.attempts_login_failed + 1
                user_update = UserUpdate(attempts_login_failed=user.attempts_login_failed)
                super().update(db,db_obj=user,obj_in=user_update)
                raise HTTPException(
                    status_code=400, detail=f"Contraseña incorrecta. Intentos restantes {settings.ATTEMPTS_LOGIN_FAILED - user.attempts_login_failed}")
        self._authenticate_user(db, user)
        return user
    # DELETE
    def _remove_user(self, db: Session, user:User):
        if user.is_superuser:
            raise HTTPException(
                    status_code=400, detail=f"El usuario administrador, no se puede eliminar")
        db.delete(user)
        db.commit()
        return user.username
    
    # FLAGS
    def is_authenticated(self, user: User) -> bool:
        return user.is_authenticated

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_blocked(self, user: User) -> bool:
        return user.is_blocked


    

    
    def _authenticate_user(self, db: Session, user: User):
        user.is_authenticated = True
        db.commit()
        db.refresh(user)


user = CRUDUser(User)
