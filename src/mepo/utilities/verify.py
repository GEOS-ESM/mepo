def valid_components(specified_comp_names, allcomps, ignore_case=False):
    """
    Validate a component name

    Arguments:
        specified_comp_names: List of component names
        allcomps: List of all components known to mepo

    Keyword arguments:
        ignore_case: should the comparison ignore case
    """

    # Make a list of all the component names depending on ignore_case
    all_component_names = [
        x.name.casefold() if ignore_case else x.name for x in allcomps
    ]

    # Loop over all the components we want to verify...
    for component_name in specified_comp_names:

        # Create a name to compare with based on ignore_case
        component_to_find = component_name.casefold() if ignore_case else component_name

        # Validate the component
        _validate_component(component_to_find, all_component_names)


def _validate_component(component, all_components):
    """
    Function to raise exception on invalid component name

    Arguments:
        component: component to validate
        all_components: List of valid components
    """

    if component not in all_components:
        raise Exception("Unknown component name [{}]".format(component))
