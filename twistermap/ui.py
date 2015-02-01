from .network import build_network, query_network

def q(thing, cache = {}):
    if 'network' not in cache:
        cache['network'] = build_network()
    return query_network(cache['network'], thing)
