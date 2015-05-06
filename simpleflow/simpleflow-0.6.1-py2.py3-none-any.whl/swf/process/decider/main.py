from __future__ import absolute_import

import sys

import swf.models

import simpleflow.swf
from . import cmdline


def load_workflow(domain, workflow_name):
    module_name, object_name = workflow_name.rsplit('.', 1)
    module = __import__(module_name, fromlist=['*'])

    workflow = getattr(module, object_name)
    return simpleflow.swf.Executor(swf.models.Domain(domain), workflow)


def load_workflows(domain, workflows):
    return [
        load_workflow(domain, workflow.strip()) for workflow in
        workflows.split(',')
    ]


def main():
    arguments = cmdline.parse_args(sys.argv[1:])
    executors = load_workflows(arguments.domain, arguments.workflow)
    decider = simpleflow.swf.process.Decider(
        executors,
        nb_children=arguments.nb_processes,
    )
    decider.is_alive = True
    decider.start()
