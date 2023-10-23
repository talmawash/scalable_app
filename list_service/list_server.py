import grpc
import logging
import psycopg2
from concurrent import futures
from protos import user_pb2_grpc, list_pb2_grpc
from shared.grpc_utils import init_grpc_telemetry
from list_service import ListService
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
    # create table for lists if it doesn't exist
    with db.cursor() as cur:
        # id, user_id, title, completed
        cur.execute(
            "CREATE TABLE IF NOT EXISTS lists (id SERIAL PRIMARY KEY, user_id INTEGER, title VARCHAR(255), completed BOOLEAN)"
        )

    init_grpc_telemetry(
        getenv("NAME"),
        getenv("ZIPKIN_URL"),
        getenv("OTEL_ENDPOINT"),
        int(getenv("PROMETHEUS_PORT")),
    )

    server = grpc.server(futures.ThreadPoolExecutor())
    
    auth_channel = grpc.insecure_channel(getenv("AUTH_SERVICE"))
    auth_stub = user_pb2_grpc.UserServiceStub(auth_channel)
    
    list_pb2_grpc.add_TodoListServicer_to_server(
        ListService(db, auth_stub), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()
