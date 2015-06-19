import sys
import json


class Config:
    def __init__(self, configFile='/etc/crowd_pam.conf'):
        try:
            with open(configFile, 'r') as f:
                raw = f.read()
                try:
                    config_data = json.loads(raw)
                    # TODO: validate the data maybe???
                    for k, v in config_data.iteritems():
                        setattr(self, k, v)

                except Exception as e:
                    raise Exception("Error Parsing JSON: {}".format(e))
        except Exception as e:
            raise Exception("Error reading configuration file: {}".format(e))

    def __del__(self):
        pass

if __name__ == "__main__":
    test_config_file = './config.conf'
    sample = {"foo": "test_foo", "bar": "test_bar"}
    try:
        print "creating test config file."
        with open(test_config_file, 'w') as f:
            f.write(json.dumps(sample))

        print "start test"
        c = Config(test_config_file)
        if c.foo == sample["foo"]:
            print "pass #1 of 2"
            if c.bar == sample["bar"]:
                print "pass #2 of 2"
            else:
                print "fail 2 of 2"
                sys.exit(1)
        else:
            print "fail 1 of 1"
            sys.exit(1)
    except Exception as e:
        print "Fail. Exception occurred: {}".format(e)
