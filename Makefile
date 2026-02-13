IP:=$$(hostname -I | awk '{print $$1}')

# Default target
all: up

# Start the container
up:
	@mkdir -p ./logs
	@chown $$(id -u):$$(id -g) ./logs
	@docker compose up -d
	@echo "Access the website: https://$(IP):8888" or https://localhost:8888

# Stop services
down:
	@docker compose down

# Remove containers, images, volumes created by this project
clean:
	@docker compose down -v --rmi all --remove-orphans

# Full clean: also prune unused Docker objects and delete ./logs
fclean: clean
	@docker system prune -af --volumes
	@rm -rf ./logs

# Rebuild from scratch
re: clean all

.PHONY: all up down clean fclean re
