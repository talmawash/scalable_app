import logging
import random
import time
import grpc
import user_pb2, user_pb2_grpc
from shared.grpc_utils import init_grpc_telemetry
from threading import Thread

allow_debug_prints = False


init_grpc_telemetry(
    "auth-client", "http://localhost:9411/api/v2/spans", None, None
)


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        # try:
        #     create_user_response = stub.CreateUser(
        #         user_pb2.CreateUserRequest(
        #             first_name="Tariq",
        #             last_name="Almawash",
        #             email="test@gmail.com",
        #             password="12345678",
        #         )
        #     )
        # except grpc.RpcError as e:
        #     if allow_debug_prints:
        #         print(e)

        login_response = stub.Login(
            user_pb2.LoginRequest(email="test@gmail.com", password="12345678")
        )
        if not login_response.token:
            if allow_debug_prints:
                print("Invalid credentials")
            return

        while True:
            for i in range(1000):
                validate_response = stub.ValidateJWT(
                    user_pb2.ValidateJWTRequest(token=login_response.token)
                )
                if allow_debug_prints:
                    print(validate_response)
                if not validate_response.valid:
                    if allow_debug_prints:
                        print("Invalid token")
                    return
            time.sleep(random.randint(1, 10))


if __name__ == "__main__":
    logging.basicConfig()
    # run multiple clients simultaneously
    simultaneous_clients = 1000
    for i in range(simultaneous_clients):
        Thread(target=run).start()
    while True:
        time.sleep(1)
