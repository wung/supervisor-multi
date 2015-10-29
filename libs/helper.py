def split_spec(spec = ''):
    specs = spec.split(':')
    section = option = group = program = None

    # section:option:group:program
    # section:option:group:*
    if len(specs) == 4:
        section, option, group, program = specs
    # section:option:program
    # section:option:*
    elif len(specs) == 3:
        section, option, program = specs
    # section:option
    # section:*
    elif len(specs) == 2:
        section, option = specs
    # section
    elif len(specs) == 1:
        pass

    return section, option, group, program

def get_conns(configs, section=None, option=None):
    conns = []

    # all connections
    if section == None:
        for key in configs.keys():
            for k in configs[key].keys():
                conns += [{'section': key, 'option': k, 'conn': configs[key][k]}]
    # one connection
    else:
        try:
            conns = [{'section': section, 'option': option, 'conn': configs[section][option]}]
        except KeyError as e:
            print 'no configs'

    # FIXME: unique conns, raise if conns duplicate
    return conns
