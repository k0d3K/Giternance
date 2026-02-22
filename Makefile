IP:=$$(hostname -I | awk '{print $$1}')

# Default target
all: up

# SSH agent setup
ssh-agent-setup:
	@test -n "$$SSH_AUTH_SOCK" || eval $$(ssh-agent -s); \
	KEY_PATH=$$(ls -1 ~/.ssh/id_* 2>/dev/null | grep -v '\.pub' | head -n1); \
	if [ -z "$$KEY_PATH" ]; then \
		echo "No private SSH key found in ~/.ssh"; \
		exit 1; \
	fi; \
	ssh-add -l | grep -q "$$(ssh-keygen -lf $$KEY_PATH | awk '{print $$3}')" || ssh-add -t 7h "$$KEY_PATH"; \

# Start the container
up: ssh-agent-setup
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
