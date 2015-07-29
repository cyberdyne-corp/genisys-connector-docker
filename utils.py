import errno


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
