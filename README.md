# Docker Kali-Linux

## Project overview

This repository provides a small Docker-based environment (Kali) managed with `docker-compose` and a `Makefile` . The Makefile exposes simple targets to bring the environment up, enter the container, stop it, fully clean the project, and rebuild from scratch.

This container also uses a **data directory** at the root of the project as a bind-mounted volume, allowing you to **easily pass files between your host and the container**.

## Prerequisites

Before using this project make sure your host has:

* `docker` install and running
* `docker-compose`
* `make` utility
* Sufficient privileges to run Docker commands.

If your user cannot run Docker without sudo, add yourself to the docker group:
```bash
sudo usermod -aG docker $USER
```
(Log out and back in for the change to take effect.)

## Usage

### Built and run

Start and enter the Kali container:
```bash
make
```

Once you'r done, just press `Ctrl + D`, or execute the `exit` command, to exit the continer.

Stop containers:
```bash
make down
```

Stop and remove images, volumes, and orphans:
```bash
make clean
```

Reset the environement back the way it was before.
```bash
make fclean
```

**Important:** `flcean` is destructive. Use with care — it removes your host `./data` directory.

You can also run `make re`. This will call `fclean` and `up` rule.

## Customization tips

* Add tools to the Kali Dockerfile (or base off an official Kali image) to include packages you need.
