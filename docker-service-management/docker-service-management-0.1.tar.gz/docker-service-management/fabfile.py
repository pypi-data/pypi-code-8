#
# Docker Container Management
#
# Copyright 2015 devops.center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from fabric.api import env, roles, run, local,put, cd, sudo, settings
from time import gmtime, strftime
import os, sys
from git import Repo

env.user="ubuntu"

def docker_container_install(containername,containerid,containerversion,ports,environmentvariables,hostentries):
    print("Executing on %(host)s as %(user)s" % env)
    container='%s:%s' % (containerid,containerversion)
    run('docker pull %s' % container)
    with settings(warn_only=True):
        run('docker stop %s' % (containername))
        run('docker rm %s' % (containername))
    expandedports=' '.join(['-p "%d:%d"'%(x,x) for x in ports])
    finalcmd='docker create %s %s -p %s -v="/data/deploy:/data/deploy" --name %s %s ' % (environmentvariables,hostentries,expandedports,containername,container)
    print finalcmd
    run(finalcmd)
    run('docker start %s' % (containername))
    run('docker inspect %s' % (containername))

webports=[80]
workerports=[6379,5555]
postgresports=[5432]

def web_install(stackname,containerversion, environmentvariables,hostentries):
    containerid="%s.web" % stackname
    docker_container_install("web",containerid,containerversion, webports,environmentvariables,hostentries)

def worker_install(stackname,containerversion, environmentvariables,hostentries):
    containerid="%s.worker" % stackname
    docker_container_install("worker",containerid,containerversion, workerports,environmentvariables,hostentries)

def postgres_master_install(containerversion,environmentvariables,hostentries):
    containername="postgresmasterdb"
    containerid="devopscenter/db_postgres" 
    docker_container_install(containername,containerid,containerversion,postgresports,environmentvariables,hostentries)

def postgres_standby_install(containerversion,environmentvariables,hostentries):
    containername="postgresstandbydb"
    containerid="devopscenter/db_postgres-standby"
    docker_container_install(containername,containerid,containerversion,postgresports,environmentvariables,hostentries)

def redis_master_install(containerversion,ports,environmentvariables,hostentries):
    containername="redismasterdb"
    containerid="devopscenter/db_postgres"
    docker_container_install(containername,containerid,containerversion,ports,environmentvariables,hostentries)

def redis_standby_install(containerversion,ports,environmentvariables,hostentries):
    containername="redisstandbydb"
    containerid="devopscenter/db_standby-redis"
    docker_container_install(containername,containerid,containerversion,ports,environmentvariables,hostentries)

