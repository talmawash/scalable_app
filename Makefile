# build docker images for auth_service and list_service
.PHONY: docker_build
docker_build:
	sudo docker build -t auth_service -f auth_service/Dockerfile .
	sudo docker build -t list_service -f list_service/Dockerfile .

# generate protobuf files
.PHONY: proto
proto:
	python -m grpc_tools.protoc -I. --python_out=./auth_service --grpc_python_out=./auth_service ./protos/user.proto
	python -m grpc_tools.protoc -I. --python_out=./list_service --grpc_python_out=./list_service ./protos/user.proto
	python -m grpc_tools.protoc -I. --python_out=./list_servic/ --grpc_python_out=./list_service ./protos/list.proto
