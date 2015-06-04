from cleo import Command, InputArgument, InputOption
from cleo import Application
from probe.params import SimParams

class PrintParamsCommand(Command):
    name = 'params:print'

    description = 'loads an input.params file and print all parameters'

    arguments = [
        {
            'name': 'input',
            'description': 'path to input.params file',
            'required': True
        }
    ]

    @staticmethod
    def execute(i, o):
        input = i.get_argument('input')

        sp = SimParams(input)

        sp.print_params('params')
        sp.print_sparams('sparams')
        sp.print_cparams('cparams')

if __name__ == '__main__':
    application = Application()
    application.add(PrintParamsCommand())
    application.run()
