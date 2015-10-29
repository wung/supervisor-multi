import ConfigParser

def parse_config(config):
    configs = {}
    conf = ConfigParser.ConfigParser()
    conf.read(config)

    for section in conf.sections():
        configs[section] = {}
        for option in conf.options(section):
            configs[section][option] = conf.get(section, option)

    return configs
