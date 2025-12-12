from app.database import admin_collection
from app.utils.security import verify_password
from app.utils.jwt_handler import create_jwt

class AuthService:

    @staticmethod
    def login(email, password):
        admin = admin_collection.find_one({"email": email})
        if not admin:
            return {"error": "Invalid credentials"}, 401

        if not verify_password(password, admin["password"]):
            return {"error": "Invalid credentials"}, 401

        token = create_jwt(str(admin["_id"]), admin["organization"])
        return {"token": token}, 200
