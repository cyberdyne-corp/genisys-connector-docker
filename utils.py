import errno
from yaml import safe_load


def load_services_from_file(filename):
    services = {}
    try:
        exec(compile(open(filename, "rb").read(), filename, 'exec'),
             {},
             services)
    except OSError as e:
        if e.errno == errno.ENOENT:
            print("No services definitions file provided.")
        else:
            print("An error occured while trying to read \
                services definitions file. Aborting.")
            raise
    return services


def load_configuration(configuration_file):
    with open(configuration_file, 'r') as stream:
        config = safe_load(stream)
        return config
