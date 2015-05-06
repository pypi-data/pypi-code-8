from __future__ import absolute_import

import logging
import multiprocessing
import os

import swf.actors
import swf.exceptions

from simpleflow.swf.process.actor import (
    MultiProcessActor,
    reset_signal_handlers,
    will_release_semaphore,
)
from simpleflow.utils import retry


logger = logging.getLogger(__name__)


class Decider(swf.actors.Decider, MultiProcessActor):
    def __init__(self, executors, nb_children=None, nb_retries=3,
                 *args, **kwargs):
        """
        The decider is an actor that reads the full history of the workflow
        execution and decides what happens next. It polls decision tasks from a
        task list and complete the task by submitting one or several decisions.
        A decision is for example scheduling an activity or completing the
        workflow execution.

        SWF ensures that only one decider gets a decision task for a workflow
        execution. A decider is stateless because it takes decisions solely
        based upon the history that comes with the decision task.

        This implementation polls a single task list within a single domain.
        It can handle several workflows on the same task list.

        :param executors: that handles workflow executions.
        :type  executors: [simpleflow.swf.Executor].
        :param nb_children: number of parallel processes that handle decision
                            tasks.
        :type  nb_children: int.

        """
        self._workflow_name = '({})'.format(','.join([
            os.path.basename(ex._workflow.name) for ex in executors
        ]))

        self.state = 'main'

        # Maps a workflow's name to its definition.
        # Used to dispatch a decision task to the corresponding workflow.
        self.workflows = {
            executor._workflow.name: executor for executor in executors
        }

        # All executors must have the same domain and task list.
        domain = executors[0].domain
        task_list = executors[0]._workflow.task_list
        for ex in executors[1:]:
            if ex.domain.name != domain.name:
                raise ValueError(
                    'all workflows must be in the same domain "{}"'.format(
                        domain.name))
            elif ex._workflow.task_list != task_list:
                raise ValueError(
                    'all workflows must have the same task list "{}"'.format(
                        task_list))

        self.nb_retries = 3

        MultiProcessActor.__init__(
            self,
            domain,
            task_list,
            nb_children=nb_children,
            *args,    # directly forward them.
            **kwargs  # directly forward them.
        )

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.set_process_name()

    @property
    def name(self):
        """
        The main purpose of this property is to find what workflow a decider
        handles.

        """
        if self._workflow_name:
            suffix = ':'.format(self._workflow_name)
        else:
            suffix = ''
        return '{}{}'.format(self.__class__.__name__, suffix)

    def poll(self, task_list=None, identity=None):
        """
        Polls a decision task represented by its token and the current workflow
        execution's history. It uses long-polling with a timeout of one minute.
        The underlying library retrieve the full history that may be split in
        several pages. It may take time.

        :param task_list: when set, it overrides the workflow's default task
                          list. The specified string must not start or end with
                          whitespace. It must not contain a : (colon), /
                          (slash), | (vertical bar), or any control characters
                          (\u0000-\u001f | \u007f - \u009f). Also, it must not
                          contain the literal string "arn".

        :type  task_list: str.
        :param identity: when set, it overrides the default decider's identity.
                         Identity of the decider making the request, which is
                         recorded in the DecisionTaskStarted event in the
                         workflow history. This enables diagnostic tracing when
                         problems arise. The form of this identity is user
                         defined. Minimum length of 0. Maximum length of 256.
        :type  identity: str.

        See also http://docs.aws.amazon.com/amazonswf/latest/apireference/API_PollForDecisionTask.html#API_PollForDecisionTask_RequestSyntax

        :returns:
            :rtype: (str, swf.models.History)

        """
        if task_list is None and self.task_list:
            task_list = self.task_list

        if identity is None and self.identity:
            identity = self.identity

        logger.debug("polling decision task on %s", task_list)
        try:
            token, history = super(Decider, self).poll(
                task_list,
                identity=identity,
            )
        except swf.exceptions.PollTimeout as err:
            logger.debug("timeout polling on %s", task_list)
            raise err
        except Exception as err:
            logger.error(
                "exception %s when polling on %s",
                str(err),
                task_list,
            )
        return (token, history)

    def decide(self, history):
        """
        Delegate the decision to the executor.

        :param history: of the workflow execution.
        :type  history: swf.models.History.
        :returns:
            :rtype: (str, [swf.models.decision.base.Decision])

        """
        self._workflow_name = history[0].workflow_type['name']
        workflow_executor = self.workflows[self._workflow_name]
        return workflow_executor.replay(history)

    @reset_signal_handlers
    @will_release_semaphore
    def handle_decision_task(self, task_list=None):
        """
        Happens in a subprocess. Polls and make decisions with respect to the
        current state of the workflow execution represented by its history.

        """
        self.state = 'polling'
        try:
            token, history = self.poll(task_list)
        except swf.exceptions.PollTimeout:
            # TODO(ggreg) move this out of the decision handling logic.
            self._children_processes.remove(os.getpid())
            return

        self.state = 'deciding'
        try:
            decisions, _ = self.decide(history)
        except Exception as err:
            message = "workflow decision failed: {}".format(err)
            logger.error(message)
            decision = swf.models.decision.WorkflowExecutionDecision()
            decision.fail(reason=swf.format.reason(message))
            decisions = [decision]

        try:
            self.state = 'completing decision task'
            complete = retry.with_delay(
                nb_times=self.nb_retries,
                delay=retry.exponential,
                logger=logger,
            )(self.complete)  # Exponential backoff on errors.
            complete(token, decisions)
        except Exception as err:
            # This embarasing because the decider cannot notify SWF of the
            # decision. As it will not try again, the decision task will
            # timeout (start_to_complete).
            logger.error("cannot complete decision task: %s", str(err))

        # TODO(ggreg) move this out of the decision handling logic.
        # This cannot work because it is executed in a subprocess.
        # Hence it does not share the parent's object.
        self._children_processes.remove(os.getpid())

    def spawn_handler(self):
        """
        Wrap decision handling in a subprocess.

        """
        try:
            self._semaphore.acquire()
        except OSError as err:
            logger.warning("cannot acquire semaphore: %s", str(err))

        if self.is_alive:
            process = multiprocessing.Process(target=self.handle_decision_task)
            process.start()
            # This is needed to wait for children when stopping the main
            # decider process.
            self._children_processes.add(process)

    def start(self):
        """
        Start the main decider process. There is no daemonization. The process
        is intented to be run inside a supervisor process.

        """
        logger.info("starting %s on domain %s", self.name, self.domain.name)
        self.set_process_name()
        while self.is_alive:
            self.spawn_handler()
