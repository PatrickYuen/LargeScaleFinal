
def set_user_for_sharding(query_set, city_id):
  if query_set._hints == None:
    query_set._hints = {'city_id' : city_id }
  else:
    query_set._hints['city_id'] = city_id
