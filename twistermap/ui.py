from random import choice

from .network import build_network, query_network

RANDOM = 1

def q(thing = RANDOM, cache = {}):
    '''
    Query for tongue-twisters related to ``thing``,
    or do a ``RANDOM`` tongue-twister. Cache the network
    after the first run.
    '''
    if 'network' not in cache:
        cache['network'] = build_network()
    if thing == RANDOM:
        thing = choice(list(cache['network'][1].keys()))
    return query_network(cache['network'], thing)

def play():
    tongue_twisters = q()
    for i in range(1000):
        if len(tongue_twisters) == 0:
            break
        tongue_twister = choice(tongue_twisters)
        yield tongue_twister
        tongue_twisters = q(tongue_twister)
