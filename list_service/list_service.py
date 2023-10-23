# TodoListService for grpc

from protos import list_pb2, list_pb2_grpc, user_pb2


class ListService(list_pb2_grpc.TodoListServicer):
    def __init__(self, db, auth_stub):
        self.db = db
        self.auth_stub = auth_stub

    def AddTodo(self, request, context):
        # verify jwt
        validation_response = self.auth_stub.ValidateJWT(
            user_pb2.ValidateJWTRequest(token=request.auth_token)
        )
        if not validation_response.valid:
            raise Exception("Invalid JWT")
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lists (user_id, title, completed) VALUES (%s, %s, %s) RETURNING *",
                [
                    validation_response.user_id,
                    request.todo.title,
                    request.todo.completed,
                ],
            )
            todo = cur.fetchone()
            return list_pb2.AddTodoResponse(
                todo=list_pb2.Todo(
                    id=todo[0], user_id=todo[1], title=todo[2], completed=todo[3]
                )
            )

    def RemoveTodo(self, request, context):
        # verify jwt
        validation_response = self.auth_stub.ValidateJWT(
            user_pb2.ValidateJWTRequest(token=request.auth_token)
        )
        if not validation_response.valid:
            raise Exception("Invalid JWT")
        if not (validation_response.user_id == request.todo.user_id):
            raise Exception("Unauthorized")
        with self.db.cursor() as cur:
            # remove based on user id and todo id
            cur.execute(
                "DELETE FROM lists WHERE user_id = %s AND id = %s RETURNING id",
                [validation_response.user_id, request.todo.id],
            )
            todo = cur.fetchone()
            return list_pb2.RemoveTodoResponse(
                result=todo is not None,
                message="Todo removed successfully" if todo else "Todo not found",
            )

    def FetchTodos(self, request, context):
        # verify jwt
        validation_response = self.auth_stub.ValidateJWT(
            user_pb2.ValidateJWTRequest(token=request.auth_token)
        )
        if not validation_response.valid:
            raise Exception("Invalid JWT")
        with self.db.cursor() as cur:
            cur.execute(
                "SELECT * FROM lists WHERE user_id = %s ORDER BY id DESC LIMIT %s OFFSET %s",
                [
                    validation_response.user_id,
                    request.page_size,
                    request.page_number * request.page_size,
                ],
            )
            todos = cur.fetchall()
            return list_pb2.FetchTodosResponse(
                todos=[
                    list_pb2.Todo(
                        id=todo[0], user_id=todo[1], title=todo[2], completed=todo[3]
                    )
                    for todo in todos
                ]
            )

    def UpdateTodo(self, request, context):
        if not (request.todo.title or request.todo.completed):
            raise Exception("Nothing to update")
        # verify jwt
        validation_response = self.auth_stub.ValidateJWT(
            user_pb2.ValidateJWTRequest(token=request.auth_token)
        )
        if not validation_response.valid:
            raise Exception("Invalid JWT")
        if not (validation_response.user_id == request.todo.user_id):
            raise Exception("Unauthorized")
        with self.db.cursor() as cur:
            query = "UPDATE lists SET"
            if request.todo.title:
                query += " title = %s"
            if request.todo.completed:
                if request.todo.title:
                    query += ","
                query += " completed = %s"
            query += " WHERE id = %s AND user_id = %s RETURNING *"
            cur.execute(
                query,
                [
                    request.todo.title,
                    request.todo.completed,
                    request.todo.id,
                    request.todo.user_id,
                ],
            )
            todo = cur.fetchone()
            return list_pb2.UpdateTodoResponse(
                todo=list_pb2.Todo(
                    id=todo[0], user_id=todo[1], title=todo[2], completed=todo[3]
                )
            )
