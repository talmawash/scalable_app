import logging
import random
import time
import threading
import grpc
from protos import user_pb2, user_pb2_grpc, list_pb2, list_pb2_grpc
from shared.grpc_utils import init_grpc_telemetry
from threading import Thread
# gui using tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Menu
from tkinter import Spinbox
from tkinter import filedialog

allow_debug_prints = False


init_grpc_telemetry(
    "list-client", "http://localhost:9411/api/v2/spans", None, None, True
)

lock = threading.Lock()
counter = 0


def run():
    global lock, counter
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)

        try:
            create_user_response = stub.CreateUser(
                user_pb2.CreateUserRequest(
                    first_name="Tariq",
                    last_name="Almawash",
                    email="test@gmail.com",
                    password="12345678",
                )
            )
        except grpc.RpcError as e:
            if allow_debug_prints:
                print(e)

        login_response = stub.Login(
            user_pb2.LoginRequest(email="test@gmail.com", password="12345678")
        )
        if not login_response.token:
            if allow_debug_prints:
                print("Invalid credentials")
            return
        with grpc.insecure_channel("localhost:50052") as channel:
            list_stub = list_pb2_grpc.TodoListStub(channel)
            
            while lock.acquire() and counter < 1:
                added = list_stub.AddTodo(
                    list_pb2.AddTodoRequest(
                        auth_token=login_response.token,
                        todo=list_pb2.Todo(
                            title="test " + str(counter),
                            completed=False,
                        ),
                    )
                )
                if counter % 2 == 0:
                    list_stub.RemoveTodo(
                        list_pb2.RemoveTodoRequest(
                            auth_token=login_response.token,
                            todo=list_pb2.Todo(
                                id=added.todo.id,
                                user_id=added.todo.user_id,
                            ),
                        )
                    )
                else:
                    list_stub.UpdateTodo(
                        list_pb2.UpdateTodoRequest(
                            auth_token=login_response.token,
                            todo=list_pb2.Todo(
                                id=added.todo.id,
                                user_id=added.todo.user_id,
                                title=added.todo.title + " - odd",
                                completed=True,
                            ),
                        )
                    )
                counter += 1
                lock.release()
                time.sleep(random.randint(1, 10))
            # fetch and print todos
            todos = list_stub.FetchTodos(
                list_pb2.FetchTodosRequest(auth_token=login_response.token, page_number = 0, page_size = 10)
            )
            for todo in todos.todos:
                print(todo)

if __name__ == "__main__":
    logging.basicConfig()
    # run multiple clients simultaneously
    simultaneous_clients = 1
    for i in range(simultaneous_clients):
        Thread(target=run).start()
    while True:
        time.sleep(1)