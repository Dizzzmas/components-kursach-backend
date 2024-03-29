from typing import Type, Optional, Union, List
from email_normalize import normalize
from flask_jwt_extended import (
    jwt_required,
    jwt_refresh_token_required,
    get_current_user,
    create_access_token,
    create_refresh_token,
)
from flask_smorest import abort, Blueprint
from jetkit.api.auth import (
    AuthModel,
    AuthRequest,
    RefreshTokenResponse,
    validate_email,
)

from db_kursach_s2.api.auth.schema import UserSchema

from marshmallow import fields as f, Schema
from db_kursach_s2.model.user import User


blp = Blueprint("Authentication", __name__, url_prefix="/api/auth")


def use_core_auth_api(auth_model: AuthModel, user_schema: Type[Schema] = UserSchema):
    class AuthResponse(Schema):
        access_token = f.String(dump_only=True)
        refresh_token = f.String(dump_only=True)
        user = f.Nested(user_schema)

    @blp.route("login", methods=["POST"])
    @blp.response(AuthResponse)
    @blp.arguments(AuthRequest, as_kwargs=True)
    def login(email: str, password: str):
        """Login with email + password."""
        cleaned_email = email.strip().lower()
        user: AuthModel = auth_model.query.filter_by(email=cleaned_email).one_or_none()
        if not user or not user.password or not user.is_correct_password(password):
            abort(401, message="Wrong user name or password")
        return auth_response_for_user(user)

    @blp.route("check", methods=["GET"])
    @jwt_required
    def check_user():
        """Check if current access token is valid."""
        return "ok"

    @blp.route("refresh", methods=["POST"])
    @jwt_refresh_token_required
    @blp.response(RefreshTokenResponse)
    def refresh_token():
        current_user = get_current_user()
        return {"access_token": create_access_token(identity=current_user)}


def use_sign_up_api(
    auth_model: AuthModel,
    user_schema: Type[Schema] = UserSchema,
    allowed_domains: Optional[Union[str, List[str]]] = "*",
    allowed_emails: Optional[List] = None,
):
    # Since sign up can require not only email/password, separate this from core auth api
    @blp.route("sign-up", methods=["POST"])
    @blp.response(user_schema)
    @blp.arguments(AuthRequest, as_kwargs=True)
    def sign_up(email: str, password: str):
        """Sign up with email and password. Possibly add other fields later."""
        cleaned_email = normalize(email.strip().lower())

        allowed = validate_email(email, allowed_domains, allowed_emails)
        if not allowed:
            abort(403, message="Domain or email is not allowed")

        existing_user: AuthModel = auth_model.query.filter_by(
            email=cleaned_email
        ).one_or_none()
        if existing_user:
            abort(400, message="There's already a registered user with this email")
        new_user = auth_model(email=email, password=password)  # type: ignore
        session = auth_model.query.session
        session.add(new_user)
        session.commit()
        return new_user


def auth_response_for_user(user: AuthModel) -> dict:
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    return {
        "access_token": access_token,  # valid for 15 minutes by default
        "refresh_token": refresh_token,  # valid for 30 days by default
        "user": user,
    }


use_core_auth_api(auth_model=User, user_schema=UserSchema)

use_sign_up_api(
    auth_model=User, user_schema=UserSchema,
)


__all__ = "blp"
