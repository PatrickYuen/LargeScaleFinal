
def set_city_for_sharding(query_set, city_name):
    query_set._hints['city_id'] = hash(city_name)

def set_shard(query_set, shard_id):
    query_set._hints['shard_id'] = shard_id