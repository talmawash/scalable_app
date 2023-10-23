# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/list.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11protos/list.proto\"E\n\x04Todo\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\r\n\x05title\x18\x03 \x01(\t\x12\x11\n\tcompleted\x18\x04 \x01(\x08\"9\n\x0e\x41\x64\x64TodoRequest\x12\x12\n\nauth_token\x18\x01 \x01(\t\x12\x13\n\x04todo\x18\x02 \x01(\x0b\x32\x05.Todo\"&\n\x0f\x41\x64\x64TodoResponse\x12\x13\n\x04todo\x18\x01 \x01(\x0b\x32\x05.Todo\"<\n\x11RemoveTodoRequest\x12\x12\n\nauth_token\x18\x01 \x01(\t\x12\x13\n\x04todo\x18\x02 \x01(\x0b\x32\x05.Todo\"u\n\x12RemoveTodoResponse\x12*\n\x06result\x18\x02 \x01(\x0e\x32\x1a.RemoveTodoResponse.Result\x12\x0f\n\x07message\x18\x03 \x01(\t\"\"\n\x06Result\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x01\"O\n\x11\x46\x65tchTodosRequest\x12\x12\n\nauth_token\x18\x01 \x01(\t\x12\x13\n\x0bpage_number\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\"*\n\x12\x46\x65tchTodosResponse\x12\x14\n\x05todos\x18\x01 \x03(\x0b\x32\x05.Todo\"<\n\x11UpdateTodoRequest\x12\x12\n\nauth_token\x18\x01 \x01(\t\x12\x13\n\x04todo\x18\x02 \x01(\x0b\x32\x05.Todo\")\n\x12UpdateTodoResponse\x12\x13\n\x04todo\x18\x01 \x01(\x0b\x32\x05.Todo2\xd7\x01\n\x08TodoList\x12.\n\x07\x41\x64\x64Todo\x12\x0f.AddTodoRequest\x1a\x10.AddTodoResponse\"\x00\x12\x37\n\nRemoveTodo\x12\x12.RemoveTodoRequest\x1a\x13.RemoveTodoResponse\"\x00\x12\x37\n\nFetchTodos\x12\x12.FetchTodosRequest\x1a\x13.FetchTodosResponse\"\x00\x12)\n\nUpdateTodo\x12\x12.UpdateTodoRequest\x1a\x05.Todo\"\x00\x62\x06proto3')



_TODO = DESCRIPTOR.message_types_by_name['Todo']
_ADDTODOREQUEST = DESCRIPTOR.message_types_by_name['AddTodoRequest']
_ADDTODORESPONSE = DESCRIPTOR.message_types_by_name['AddTodoResponse']
_REMOVETODOREQUEST = DESCRIPTOR.message_types_by_name['RemoveTodoRequest']
_REMOVETODORESPONSE = DESCRIPTOR.message_types_by_name['RemoveTodoResponse']
_FETCHTODOSREQUEST = DESCRIPTOR.message_types_by_name['FetchTodosRequest']
_FETCHTODOSRESPONSE = DESCRIPTOR.message_types_by_name['FetchTodosResponse']
_UPDATETODOREQUEST = DESCRIPTOR.message_types_by_name['UpdateTodoRequest']
_UPDATETODORESPONSE = DESCRIPTOR.message_types_by_name['UpdateTodoResponse']
_REMOVETODORESPONSE_RESULT = _REMOVETODORESPONSE.enum_types_by_name['Result']
Todo = _reflection.GeneratedProtocolMessageType('Todo', (_message.Message,), {
  'DESCRIPTOR' : _TODO,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:Todo)
  })
_sym_db.RegisterMessage(Todo)

AddTodoRequest = _reflection.GeneratedProtocolMessageType('AddTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _ADDTODOREQUEST,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:AddTodoRequest)
  })
_sym_db.RegisterMessage(AddTodoRequest)

AddTodoResponse = _reflection.GeneratedProtocolMessageType('AddTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _ADDTODORESPONSE,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:AddTodoResponse)
  })
_sym_db.RegisterMessage(AddTodoResponse)

RemoveTodoRequest = _reflection.GeneratedProtocolMessageType('RemoveTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVETODOREQUEST,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:RemoveTodoRequest)
  })
_sym_db.RegisterMessage(RemoveTodoRequest)

RemoveTodoResponse = _reflection.GeneratedProtocolMessageType('RemoveTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMOVETODORESPONSE,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:RemoveTodoResponse)
  })
_sym_db.RegisterMessage(RemoveTodoResponse)

FetchTodosRequest = _reflection.GeneratedProtocolMessageType('FetchTodosRequest', (_message.Message,), {
  'DESCRIPTOR' : _FETCHTODOSREQUEST,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:FetchTodosRequest)
  })
_sym_db.RegisterMessage(FetchTodosRequest)

FetchTodosResponse = _reflection.GeneratedProtocolMessageType('FetchTodosResponse', (_message.Message,), {
  'DESCRIPTOR' : _FETCHTODOSRESPONSE,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:FetchTodosResponse)
  })
_sym_db.RegisterMessage(FetchTodosResponse)

UpdateTodoRequest = _reflection.GeneratedProtocolMessageType('UpdateTodoRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATETODOREQUEST,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:UpdateTodoRequest)
  })
_sym_db.RegisterMessage(UpdateTodoRequest)

UpdateTodoResponse = _reflection.GeneratedProtocolMessageType('UpdateTodoResponse', (_message.Message,), {
  'DESCRIPTOR' : _UPDATETODORESPONSE,
  '__module__' : 'protos.list_pb2'
  # @@protoc_insertion_point(class_scope:UpdateTodoResponse)
  })
_sym_db.RegisterMessage(UpdateTodoResponse)

_TODOLIST = DESCRIPTOR.services_by_name['TodoList']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TODO._serialized_start=21
  _TODO._serialized_end=90
  _ADDTODOREQUEST._serialized_start=92
  _ADDTODOREQUEST._serialized_end=149
  _ADDTODORESPONSE._serialized_start=151
  _ADDTODORESPONSE._serialized_end=189
  _REMOVETODOREQUEST._serialized_start=191
  _REMOVETODOREQUEST._serialized_end=251
  _REMOVETODORESPONSE._serialized_start=253
  _REMOVETODORESPONSE._serialized_end=370
  _REMOVETODORESPONSE_RESULT._serialized_start=336
  _REMOVETODORESPONSE_RESULT._serialized_end=370
  _FETCHTODOSREQUEST._serialized_start=372
  _FETCHTODOSREQUEST._serialized_end=451
  _FETCHTODOSRESPONSE._serialized_start=453
  _FETCHTODOSRESPONSE._serialized_end=495
  _UPDATETODOREQUEST._serialized_start=497
  _UPDATETODOREQUEST._serialized_end=557
  _UPDATETODORESPONSE._serialized_start=559
  _UPDATETODORESPONSE._serialized_end=600
  _TODOLIST._serialized_start=603
  _TODOLIST._serialized_end=818
# @@protoc_insertion_point(module_scope)
