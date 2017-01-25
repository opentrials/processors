import os
import json
import logging

logger = logging.getLogger(__name__)

PHASE_VARIATION_PATH = os.path.join(os.path.dirname(__file__),
                                    'phases_variations.json')


def get_normalized_phase(phase):
    """ Receives a phase as an input and normalizes it if possible.
        Else, returns the unormalized phase.

        :param:
            phase (str): unormalized phase

        :return:
            phase_suggestions (list): normalized phase suggestions
    """
    with open(PHASE_VARIATION_PATH) as phase_variation_file:
        phase_variation_map = json.load(phase_variation_file)
    phase_suggestions = None
    if phase in phase_variation_map.keys():
        phase_suggestions = phase_variation_map[phase]
    else:
        logger.debug('Unable to normalize phase \'%s\'', phase)
        if phase:
            phase_suggestions = [phase]
    return phase_suggestions
