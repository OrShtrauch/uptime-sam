#!/bin/bash

docker-compose down

npm run build-docker

docker build -t jenkins-fetcher -f jenkins/Dockerfile .

docker compose up -d