#!/usr/bin/env python

import os
import sys
import docker
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def help():
  print('Perform a Blue/Green deployment of petclinic to Docker.')
  print('Required environment variables:')
  print('IMAGE - the image to deploy (ex: "petclinic")')
  print('NETWORK - the network to attach deployments to (ex: "local_network")')
  print('ENVIRONMENTS - environments to deploy to (ex: "prod1 prod2 prod3")')

product = 'petclinic'
image = os.environ.get('IMAGE', None) # Ex: 'petclinic-tomcat:latest'
network = os.environ.get('NETWORK', None) # Ex: 'traefik-network'
environments = os.environ.get('ENVIRONMENTS', None).split() # Ex: 'prod1 prod2'

print(os.listdir(os.getcwd()))

# Validate parameters
if not all([image, network, environments]):
    print('Missing environment variable(s). See help:')
    help()
    sys.exit(1)

def abort_deployment(green_deployments):
  """Forcibly remove all green deployment containers"""
  for container in green_deployments:
    container.remove(force=True)

green_containers = []

# Deploy green containers
for env in environments:
  name = '%s-%s-green' % (env, product)
  labels = {
    'traefik.backend': name,
    'traefik.frontend.rule': '%s.%s.docker.localhost' % (env, product)
  }
  print('Deploying %s' % name)
  green_containers.append(
    client.containers.run(image, detach=True, network=network,
                          name=name, ports={8080:None}, labels=labels)
  )

# Smoke test green containers
for container in green_containers:
  regression_suite_path = os.path.join(os.getcwd(), 'regression-suite')
  volumes = {os.getcwd(): {'bind': '/spring-petclinic', 'mode': 'ro'}}
  command = 'echo "mocking regression test..."' # 'mvn clean -B test -DPETCLINIC_URL=http://%s:8080/petclinic/' % (container.name)

  try:
    print('Running smoke test on %s' % container.name)
    client.containers.run('maven:3.5.0', network=network, volumes=volumes,
                          working_dir='/spring-petclinic/regression-suite',
                          command=command, remove=True)

  except docker.errors.ContainerError as e:
    print(e)
    print('Smoke test failed for %s' % container.name)
    print('Aborting deployment')
    abort_deployment(green_deployments)
    sys.exit(1)

print('Removing blue containers')
for container in client.containers.list():
  if product in container.name and not container.name.endswith('-green'):
    container.remove(force=True)

print('Renaming green containers')
for container in green_containers:
  container.rename(container.name[:-6])

print('Blue/Green deployment complete')
