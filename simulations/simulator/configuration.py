def get_initial_configuration():
    return {
        'field_size': 100,
        'exp': 3,
        'sd': 1,
        'field_fertility': 5,
        'vitality': 50,
        'charisma': 50,
        'life_decrease': 1,
        'life_increase': 20,
        'prob_decrease': 0.2,
    }


def configure(parameters):
    configuration = get_initial_configuration()
    if parameters['field_fertility']:
        configuration['field_fertility'] = parameters['field_fertility']
    if parameters['vitality']:
        configuration['vitality'] = parameters['vitality']
    if parameters['charisma']:
        configuration['charisma'] = parameters['charisma']
    return configuration
