#!/bin/bash
# ------------------------------------------------------------------
# [Badr Larhdir] test_docker.sh
#
#          This script is a to ensure the robustness and reliability of the deployed model 
#          It uses the the docker-compose.test.yml file for the test
#          It will run the test container and then stop it

# This command does the following:
#   -f docker-compose.test.yml: Tells Docker Compose to use the test 
#      configuration file.
#   --abort-on-container-exit: Stops all containers if any container was stopped 
#     Since the test container will exit after running tests, this flag ensures 
#     that Docker Compose also stops.
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

docker-compose -f docker-compose.test.yml down