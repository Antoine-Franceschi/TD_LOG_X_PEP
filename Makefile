app_name = gunicorn_flask

build:
	@docker build -t $(app_name) .
run:
# --detach option is used to run in background, so no output to terminal
	docker run --detach -p 5000:5000 $(app_name)
kill:
	@echo 'Killing container...'
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker stop
print_ip:
	@docker ps | grep $(app_name) | awk '{print $1;}' | xargs docker inspect | grep IPAddress