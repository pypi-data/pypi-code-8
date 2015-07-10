import csv
import json
import itertools
import os
import sys

__version__ = "0.7.0"


def main():
    if len(sys.argv) < 2:
        print "Usage: generate_sweep <ExperimentSpecification.json>"
        exit(0)
    filename = sys.argv[1]

    try:
        generate_scenarios(filename)
    except KeyError as e:
        print "Sweep generation failed"
        print "Can't find parameter %s" % e


def generate_scenarios(filename, base_dir=None):
    with open(filename) as fp:
        experiment_specification = json.load(fp)
    exp = ExperimentSpecification(experiment_specification)
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(filename))
    exp.generate_scenarios(base_dir)


def update_emod_parameter(config, *parameter_path, **kwargs):
    # Consider this a prototype of xpath parser implementation (with no eval, unlike jsonpath!)
    sub_section_of_config = config
    prev_sub_section_of_config = sub_section_of_config

    if len(parameter_path) == 0:
        raise TypeError
    param = parameter_path[-1]  # Last parameter in the parameter_path

    for param in parameter_path:
        if ']' in param:
            # 0] , 1] etc  - index in array
            param = int(param[:-1])
        prev_sub_section_of_config = sub_section_of_config
        sub_section_of_config = sub_section_of_config[param]
    prev_sub_section_of_config[param] = kwargs["value"]
    return config


class ExperimentSpecification(object):
    def __init__(self, experiment_specification):
        if isinstance(experiment_specification, str):
            experiment_specification = json.loads(experiment_specification)
        if hasattr(experiment_specification, "read"):
            experiment_specification = json.load(experiment_specification)
        if not isinstance(experiment_specification, dict):
            raise TypeError("experiment_specification should be a string, open file or a dict")
        self.experiment_specification = experiment_specification

    def combinations(self):
        sweeps = []
        sweep_names = []
        for placeholder, value in self.experiment_specification["simple_sweep"].iteritems():
            if not isinstance(value, list):
                value = [value]
            sweeps.append(value)
            sweep_names.append(placeholder)
        for sweep in itertools.product(*sweeps):
            yield dict(zip(sweep_names, sweep))

    def generate_scenarios(self, base_dir=None):
        cwd = os.curdir
        if base_dir is not None and base_dir != '':
            os.chdir(base_dir)
        try:
            template_files = {}

            for filename in self.experiment_specification["input files"]:
                with open(filename) as fp:
                    template_files[filename] = json.load(fp)

            new_files = template_files
            scenario_number = 0
            information = []
            for combination in self.combinations():
                scenario_number += 1

                # generate files from the scenario template files
                for placeholder in combination:
                    replacement = combination[placeholder]
                    filename = placeholder.split("/")[0]
                    if filename not in template_files:
                        # Assume config.json.
                        # Warning - danger zone if there is a typo in filename
                        filename = "config.json"
                        placeholder = placeholder.replace('[', '/').split("/")
                        placeholder.insert(0, "parameters")
                    else:
                        placeholder = placeholder.replace('[', '/').split("/")[1:]
                    new_files[filename] = update_emod_parameter(new_files[filename], *placeholder, value=replacement)

                # save files to a subfolder
                try:
                    os.mkdir(str(scenario_number))
                except OSError:
                    pass

                for filename in new_files:
                    with open(os.path.join(str(scenario_number), filename), "w") as fp:
                        json.dump(new_files[filename], fp=fp, indent=4, sort_keys=True)
                combination["scenario"] = scenario_number
                information.append(combination)

            fp = open("scenarios.csv", "wb")
            fieldnames = information[0].keys()
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for row in information:
                writer.writerow(row)
            fp.close()
        except:
            os.chdir(cwd)
            raise

if __name__ == "__main__":
    main()
