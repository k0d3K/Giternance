<img src="./frontend/public/Giternance.png" width="500">

## Project overview

This tool has been designed to **smartly synchronize two Git repositories**.  
It works by automatically copying commits from a source repository to a destination repository at the times you choose, making your commit history appear as if you worked at those hours.

It was **initially designed for 42 students** following the **42 Alternance program**, where automating commits can help simulate consistent activity across personal or project repositories.

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

### Setup

Start the service:
```bash
make
```
This will gave you the address for the connection

Stop the service:
```bash
make down
```

Stop and clean:
```bash
make clean
```

Clear the precistant logs.
```bash
make fclean
```

**Important:** `flcean` is destructive. Use with care — you will not be able to get your logs back.

You can also run `make re`. This will call `clean` and `up` rule.

## Usage

1. Access the website
2. Provide the links of the source and destination repositories
3. Select the hours you want your commits to appear
4. Start the synchronization

That's it 😃
