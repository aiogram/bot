# aiogram_bot

This bot is used as example of usage [aiogram](https://github.com/aiogram/aiogram) framework 
and as admin-helper in our community chats.

## What this bot can do?

- May exist
- Watch new chat members and filter users (ask question and restrict user)
- Has simple admin commands for making restrictions
- Chat admins notifier (command which send message to all admins when someone is report message in chat)
- Can be translated (en, ru, uk languages)

## Development

### System dependencies

- Python 3.7
- pipenv
- Docker
- docker-compose
- make

### Setup environment

- Install dependencies in venv: `pipenv install --dev`
- Copy `.env.dist` to `.env` file and change values in this file
- Run databases in docker: `make docker-up-db`
- Apply migrations: `make migrate`

### Project structure

- Application package is in `app`
- All text translations is placed in `locales`
- Migrations is placed in `migrations`
- Entry-point is `app/__main__.py` (Can be executed as `python -m app`)
...

### Contributing

Before you will make commit need to run `black`, `isort` and `Flake8` via command `make lint`
If you change Database models you will need to generate migrations: `make migration message="do something"`

## Deployment

Here listed only Docker deployment methods. 
That's mean you can't read here how to deploy the bot with other methods instead of Docker 
but you can do that manually.

Also this bot can't be normally started in Docker with polling mode 
because in this mode aiohttp server will be not started and healthcheck can not be started.

### docker-compose

Pre-requirements:
- Docker
- docker-compose

Steps:
- Prepare `.env` file
- ... (TODO)
- `make app-create` - for first deploy, for updating or restarting

Stopping:
- `make docker-stop`

Destroying (with volumes):
- `make docker-destroy`

### Docker Swarm

Pre-requirements:
- Docker (with activated swarm mode)
- traefik 2.0 in Docker (with overlay network named `web`)

### Commands:

...

### How this bot is deployed now?

In Docker Swarm at [Illemius](https://illemius.xyz) with CI/CD

Steps:
1. GitHub Actions:
    1. Build docker image
    1. Publish it to the private **Illemius** Docker registry
    1. Trigger Portainer webhook in the **Illemius** cluster via cURL
1. Portainer will trigger updating of the bot service
1. Docker run new instance of container at specified node
    1. When container is started by first step it will run migrations
1. Docker wait until new instance will be healthy
1. Traefik watch Docker container and update the routes when new one is available
1. Stop old instance of Bot container
