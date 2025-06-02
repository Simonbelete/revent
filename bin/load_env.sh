#!/bin/sh

echo "Loading env..."

if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

##################### Inject env to api/ 
envsubst < api/.env.template > api/.env

##################### Inject env to admin_panel/
envsubst < admin_panel/.env.template > admin_panel/.env

##################### Inject env to client/
envsubst < client/.env.template > client/.env





#################### Inject env to casbin server
# envsubst < config/casbin_server/connection_config.template.json > config/casbin_server/connection_config.json
#################### Inject env to docker-compose.yml
# envsubst < infra.template.yml > infra.yml
# envsubst < docker-compose.template.yml > docker-compose.yml