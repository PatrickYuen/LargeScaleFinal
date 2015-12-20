
def set_city_for_sharding(query_set, city_id):
	query_set._hints['city_id'] = city_id

def set_shard(query_set, shard_id):
    query_set._hints['shard_id'] = shard_id