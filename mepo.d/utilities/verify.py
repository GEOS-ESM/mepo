def valid_components(specified_components, allcomponents):
    for compname in specified_components:
        if compname not in allcomponents:
            raise Exception('Unknown component name [{}]'.format(compname))
