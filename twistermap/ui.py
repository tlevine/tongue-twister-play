from random import choice

from .network import build_network, query_network

RANDOM = 1

def q(thing = RANDOM, cache = {}):
    if 'network' not in cache:
        cache['network'] = build_network()
    if thing == RANDOM:
        thing = choice(list(cache['network'][1].keys()))
    return query_network(cache['network'], thing)
