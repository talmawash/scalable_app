import grpc
import logging
from protos import user_pb2_grpc
import psycopg2
from concurrent import futures
from shared.grpc_utils import init_grpc_telemetry
from user_service import UserService
from os import getenv
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    logging.basicConfig()

    db = psycopg2.connect(
        host=getenv("POSTGRES_HOST"),
        port=int(getenv("POSTGRES_PORT")),
        user=getenv("POSTGRES_USER"),
        password=getenv("POSTGRES_PASSWORD"),
        database=getenv("POSTGRES_DB"),
    )
    db.autocommit = True
    # create table for users if it doesn't exist
    with db.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), password VARCHAR(512),  UNIQUE(email))"
        )

    
    init_grpc_telemetry(getenv("NAME"), getenv("ZIPKIN_URL"), getenv("OTEL_ENDPOINT"), int(getenv("PROMETHEUS_PORT")))

    server = grpc.server(futures.ThreadPoolExecutor())

    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(database=db, service_name=getenv("NAME"), secret=getenv("SECRET")), server)
    
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()