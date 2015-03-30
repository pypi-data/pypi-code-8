########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


from cloudify import manager
from cloudify import logs
from cloudify.logs import CloudifyPluginLoggingHandler
from cloudify.exceptions import NonRecoverableError


class Endpoint(object):

    def __init__(self, ctx):
        self.ctx = ctx

    def get_node(self, node_id):
        raise NotImplementedError('Implemented by subclasses')

    def get_node_instance(self, node_instance_id):
        raise NotImplementedError('Implemented by subclasses')

    def update_node_instance(self, node_instance):
        raise NotImplementedError('Implemented by subclasses')

    def get_blueprint_resource(self, blueprint_id, resource_path):
        raise NotImplementedError('Implemented by subclasses')

    def download_blueprint_resource(self,
                                    blueprint_id,
                                    resource_path,
                                    logger,
                                    target_path=None):
        raise NotImplementedError('Implemented by subclasses')

    def get_provider_context(self):
        raise NotImplementedError('Implemented by subclasses')

    def get_bootstrap_context(self):
        raise NotImplementedError('Implemented by subclasses')

    def get_logging_handler(self):
        raise NotImplementedError('Implemented by subclasses')

    def send_plugin_event(self,
                          message=None,
                          args=None,
                          additional_context=None):
        raise NotImplementedError('Implemented by subclasses')

    def get_host_node_instance_ip(self,
                                  host_id,
                                  properties=None,
                                  runtime_properties=None):
        """
        See ``manager.get_node_instance_ip``
        (this method duplicates its logic for the
        sake of some minor optimizations and so that it can be used in local
        context).
        """
        # properties and runtime_properties are either both None or
        # both not None
        if not host_id:
            raise NonRecoverableError('host_id missing')
        if runtime_properties is None:
            instance = self.get_node_instance(host_id)
            runtime_properties = instance.runtime_properties
        if runtime_properties.get('ip'):
            return runtime_properties['ip']
        if properties is None:
            # instance is not None (see comment above)
            node = self.get_node(instance.node_id)
            properties = node.properties
        if properties.get('ip'):
            return properties['ip']
        raise NonRecoverableError('could not find ip for host node instance: '
                                  '{0}'.format(host_id))

    def evaluate_functions(self, payload):
        raise NotImplementedError('Implemented by subclasses')

    def _evaluate_functions_impl(self,
                                 payload,
                                 evaluate_functions_method):
        from cloudify import context
        evaluation_context = {}
        if self.ctx.type == context.NODE_INSTANCE:
            evaluation_context['self'] = self.ctx.instance.id
        elif self.ctx.type == context.RELATIONSHIP_INSTANCE:
            evaluation_context.update({
                'source': self.ctx.source.instance.id,
                'target': self.ctx.target.instance.id
            })
        return evaluate_functions_method(deployment_id=self.ctx.deployment.id,
                                         context=evaluation_context,
                                         payload=payload)


class ManagerEndpoint(Endpoint):

    def __init__(self, ctx):
        super(ManagerEndpoint, self).__init__(ctx)

    def get_node(self, node_id):
        client = manager.get_rest_client()
        return client.nodes.get(self.ctx.deployment.id, node_id)

    def get_node_instance(self, node_instance_id):
        return manager.get_node_instance(node_instance_id)

    def update_node_instance(self, node_instance):
        return manager.update_node_instance(node_instance)

    def get_blueprint_resource(self, blueprint_id, resource_path):
        return manager.get_blueprint_resource(blueprint_id, resource_path)

    def download_blueprint_resource(self,
                                    blueprint_id,
                                    resource_path,
                                    logger,
                                    target_path=None):
        return manager.download_blueprint_resource(blueprint_id,
                                                   resource_path,
                                                   logger,
                                                   target_path)

    def get_provider_context(self):
        return manager.get_provider_context()

    def get_bootstrap_context(self):
        return manager.get_bootstrap_context()

    def get_logging_handler(self):
        return CloudifyPluginLoggingHandler(self.ctx,
                                            out_func=logs.amqp_log_out)

    def send_plugin_event(self,
                          message=None,
                          args=None,
                          additional_context=None):
        logs.send_plugin_event(self.ctx,
                               message,
                               args,
                               additional_context,
                               out_func=logs.amqp_event_out)

    def evaluate_functions(self, payload):
        client = manager.get_rest_client()

        def evaluate_functions_method(deployment_id, context, payload):
            return client.evaluate.functions(deployment_id,
                                             context,
                                             payload)['payload']
        return self._evaluate_functions_impl(payload,
                                             evaluate_functions_method)


class LocalEndpoint(Endpoint):

    def __init__(self, ctx, storage):
        super(LocalEndpoint, self).__init__(ctx)
        self.storage = storage

    def get_node(self, node_id):
        return self.storage.get_node(node_id)

    def get_node_instance(self, node_instance_id):
        instance = self.storage.get_node_instance(node_instance_id)
        return manager.NodeInstance(
            node_instance_id,
            instance.node_id,
            runtime_properties=instance.runtime_properties,
            state=instance.state,
            version=instance.version,
            host_id=instance.host_id,
            relationships=instance.relationships)

    def update_node_instance(self, node_instance):
        return self.storage.update_node_instance(
            node_instance.id,
            runtime_properties=node_instance.runtime_properties,
            state=None,
            version=node_instance.version)

    def get_blueprint_resource(self, blueprint_id, resource_path):
        return self.storage.get_resource(resource_path)

    def download_blueprint_resource(self,
                                    blueprint_id,
                                    resource_path,
                                    logger,
                                    target_path=None):
        return self.storage.download_resource(resource_path,
                                              target_path)

    def get_provider_context(self):
        # TODO
        return {}

    def get_bootstrap_context(self):
        # TODO
        return {}

    def get_logging_handler(self):
        return CloudifyPluginLoggingHandler(self.ctx,
                                            out_func=logs.stdout_log_out)

    def send_plugin_event(self,
                          message=None,
                          args=None,
                          additional_context=None):
        logs.send_plugin_event(self.ctx,
                               message,
                               args,
                               additional_context,
                               out_func=logs.stdout_event_out)

    def evaluate_functions(self, payload):
        def evaluate_functions_method(deployment_id, context, payload):
            return self.storage.env.evaluate_functions(payload=payload,
                                                       context=context)
        return self._evaluate_functions_impl(
            payload, evaluate_functions_method)
