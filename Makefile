del-network:
	docker network rm public
network:
	docker network create -d overlay --attachable public

compose:
	docker-compose up

deploy: network compose