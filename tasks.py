"""
Invoke tasks, for people too lazy to type. (c) 2021 Calvin Remsburg
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
from invoke import task

### ---------------------------------------------------------------------------
### DOCKER PARAMETERS
### ---------------------------------------------------------------------------
DOCKER_COMPOSE_FILE = "files/docker/docker-compose.yml"

### ---------------------------------------------------------------------------
### SYSTEM PARAMETERS
### ---------------------------------------------------------------------------
PWD = os.getcwd()

### ---------------------------------------------------------------------------
### DOCKER CONTAINER BUILD
### ---------------------------------------------------------------------------
@task
def build(context, docker_compose_file=DOCKER_COMPOSE_FILE):
    # Build our docker image
    context.run(
        f"docker-compose -f {docker_compose_file} -p elk build",
    )

### ---------------------------------------------------------------------------
### START CONTAINERS
### ---------------------------------------------------------------------------
@task
def start(context, docker_compose_file=DOCKER_COMPOSE_FILE):
    # Get access to the BASH shell within our container
    print("starting the applications in the background")
    context.run(
        f"docker-compose -f {docker_compose_file} up -d",
    )

### ---------------------------------------------------------------------------
### STOP AND CLEANUP
### ---------------------------------------------------------------------------
@task
def cleanup(context, docker_compose_file=DOCKER_COMPOSE_FILE):
    print("stopping and removing our containers")
    context.run(
        f"docker-compose -f {docker_compose_file} stop && docker-compose -f {docker_compose_file} rm -f",
    )

### ---------------------------------------------------------------------------
### WATCH LOGS
### ---------------------------------------------------------------------------
@task
def logs(context, docker_compose_file=DOCKER_COMPOSE_FILE):
    context.run(
        f"docker-compose -f {docker_compose_file} logs -f",
    pty=True,
    )
