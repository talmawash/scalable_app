from grpc import StatusCode
from opentelemetry import metrics
from protos.user_pb2 import UserResponse, LoginResponse, ValidateJWTResponse
from protos.user_pb2_grpc import UserServiceServicer
import jwt
from datetime import datetime, timedelta
from psycopg2 import sql
import bcrypt


class UserService(UserServiceServicer):
    def __init__(self, database, service_name, secret):
        metrics_provider = metrics.get_meter_provider()
        self.request_counter = metrics_provider.get_meter(service_name).create_counter(
            "user_service_requests", "requests", "number of request thus far"
        )
        self.login_counter = metrics_provider.get_meter(service_name).create_counter(
            "user_service_login", "requests", "number of login requests thus far"
        )
        self.create_user_counter = metrics_provider.get_meter(
            service_name
        ).create_counter(
            "user_service_create_user",
            "requests",
            "number of create_user requests thus far",
        )
        self.validate_jwt_counter = metrics_provider.get_meter(
            service_name
        ).create_counter(
            "user_service_validate_jwt",
            "requests",
            "number of validate_jwt requests thus far",
        )
        self.db = database
        self.secret = secret

    def CreateUser(self, request, context):
        try:
            self.request_counter.add(1)
            self.create_user_counter.add(1)
            with self.db.cursor() as cur:
                # check if user already exists, otherwise create user.
                # can be consolidated into one query, but it'll require hashing the password before executing the query
                cur.execute(
                    sql.SQL("SELECT 1 FROM users WHERE email = %s"), [request.email]
                )
                if cur.fetchone():
                    raise Exception("User already exists")
                hashed_password = bcrypt.hashpw(
                    request.password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                cur.execute(
                    sql.SQL(
                        "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s) RETURNING *"
                    ),
                    [
                        request.first_name,
                        request.last_name,
                        request.email,
                        hashed_password,
                    ],
                )
                user = cur.fetchone()

            self.db.commit()
            return UserResponse(id=user[0])
        except Exception as e:
            context.set_details(str(e))
            context.set_code(StatusCode.INTERNAL)
            return UserResponse()

    def Login(self, request, context):
        try:
            self.request_counter.add(1)
            self.login_counter.add(1)
            with self.db.cursor() as cur:
                cur.execute(
                    sql.SQL("SELECT id, password FROM users WHERE email = %s"),
                    [request.email],
                )
                user = cur.fetchone()
                if not user or not bcrypt.checkpw(
                    request.password.encode("utf-8"), user[1].encode("utf-8")
                ):
                    return None
                payload = {
                    "sub": user[0],
                    "exp": datetime.utcnow() + timedelta(minutes=30),
                }
                token = jwt.encode(payload, self.secret, algorithm="HS256")
            return LoginResponse(token=token)
        except Exception as e:
            context.set_details(str(e))
            context.set_code(StatusCode.INTERNAL)
            return LoginResponse()

    def ValidateJWT(self, request, context):
        try:
            self.request_counter.add(1)
            self.validate_jwt_counter.add(1)
            payload = jwt.decode(request.token, self.secret, algorithms=["HS256"])
            user_id = payload.get("sub")
            if not user_id:
                return ValidateJWTResponse(valid=False)
            with self.db.cursor() as cur:
                cur.execute(sql.SQL("SELECT id FROM users WHERE id = %s"), [user_id])
                user = cur.fetchone()

            return ValidateJWTResponse(
                valid=user is not None, user_id=user[0] if user else None
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(StatusCode.INTERNAL)
            return ValidateJWTResponse()
