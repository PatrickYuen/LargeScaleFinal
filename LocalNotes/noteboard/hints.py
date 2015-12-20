
def set_city_for_sharding(query_set, city_id):
    query_set._hints['city_id'] = city_id

def set_user_for_sharding(query_set, user_id):
    query_set._hints['user_id'] = user_id