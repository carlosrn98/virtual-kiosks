# virtual-kiosks
Graduation project.

## Development
### Install Docker and docker compose
First, you need [Docker](https://docs.docker.com/engine/install/ubuntu/) and [docker compose](https://docs.docker.com/compose/install/linux/) on your local machine.

### Running dev environment
To run the dev environment, you need to be in the `virtual-kiosks` directory and run:

```shell
docker compose up -d --build
```

This command will build the image from the [`Dockerfile`](https://github.com/carlosrn98/virtual-kiosks/blob/main/Dockerfile) and will run the container from that image and for the `Postgres` database, that can also be found in the [`docker-compose.yml`](https://github.com/carlosrn98/virtual-kiosks/blob/ff4b922b0c6551b68194fd1b0cc00c990dcc8a5a/docker-compose.yml#L22) file.

### Running commands inside any of the containers
First and foremost, the names of the containers should be the same for everyone, but in case you are in doubt, you can always get them by running `docker ps`.

To run the command inside a running container, there are a couple of ways but we are going to run it through `docker compose`:

```shell
docker compose exec <container_name> some command
```

For instance, to get the current user from the `db` container:
```shell
docker compose exec db whoami
```

Or if you want to log into a container, run:
```shell
docker compose exec -it web bash
```

### Developing for the Django web application
The web application runs on `localhost:8000`, while the `Postgres` database runs on `localhost:5432`.

If you are making changes in any of the files inside the `app` dircetory, there's no need to do anything to see the changes you made, since the container already has an [attached](https://github.com/carlosrn98/virtual-kiosks/blob/ff4b922b0c6551b68194fd1b0cc00c990dcc8a5a/docker-compose.yml#L8) volume, so the changes you make from your IDE, or by changing any file should be visible instantly (as long as the containers are up and running, which again you can check by running `docker ps` and seeing both containers listed there running).

### Creating new views
If you are creating any `views` for the project, be sure to add them to [`app/website/views.py`](https://github.com/carlosrn98/virtual-kiosks/blob/main/app/website/views.py) and then add that view to the list of [urls](https://github.com/carlosrn98/virtual-kiosks/blob/main/app/website/urls.py). 

You can take the `index` endpoint as an example. The view is declared [here](https://github.com/carlosrn98/virtual-kiosks/blob/ff4b922b0c6551b68194fd1b0cc00c990dcc8a5a/app/website/views.py#L4) and then, to access it you need to declare it [here](https://github.com/carlosrn98/virtual-kiosks/blob/ff4b922b0c6551b68194fd1b0cc00c990dcc8a5a/app/website/urls.py#L4-L5).
