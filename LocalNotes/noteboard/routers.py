NUM_LOGICAL_SHARDS = 16
NUM_PHYSICAL_SHARDS = 2

LOGICAL_TO_PHYSICAL = ('db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2',
						'db1', 'db2', 'db1', 'db2', 'db1', 'db2', 'db1', 'db2')

def bucket_cities_into_shards(city_ids):
  d = {}
  for id in city_ids:
    shard = logical_shard_for_city(id)
    if not shard in d:
      d[shard] = []
    d[shard].append(id)
  return d
  return [str(x) for x in range(NUM_LOGICAL_SHARDS)]

def logical_to_physical(logical):
  if logical >= NUM_LOGICAL_SHARDS or logical < 0:
    raise Exception("shard out of bounds %d" % logical)
  return LOGICAL_TO_PHYSICAL[logical] 
 
def logical_shard_for_city(city_id):
  print "Looking for shard for city %d" % city_id
  return city_id % NUM_LOGICAL_SHARDS

class CityRouter(object):

	def _database_of(self, city_id):
		return logical_to_physical(logical_shard_for_city(city_id))

	def _db_for_read_write(self, model, **hints):
		""" """
		
		# Auth reads always go to the auth sub-system
		if model._meta.app_label == 'auth':
			return 'authdb'
		
		# For now, sessions are stored on the auth sub-system, too.
		if model._meta.app_label == 'admin':
			return 'authdb'
			
		db = 'db1' 
		try:
			if 'shard_id' in hints:
				db = hints['shard_id']
			else:
				db = self._database_of(hints['city_id'])
		except AttributeError:
			# For the city model the key is id.
			db = self._database_of(instance.id)
		except KeyError:
			try:
				#No instance means it's a new city object
				db = 'cities'
			except KeyError:
				print "No instance in hints"
		print "Returning", db
		return db
  
	def db_for_read(self, model, **hints):
		""" """
		return self._db_for_read_write(model, **hints)
  
	def db_for_write(self, model, **hints):
		""" """
		return self._db_for_read_write(model, **hints)

	def allow_relation(self, obj1, obj2, **hints):
		if (obj1._meta.app_label == 'auth' and obj2._meta.app_label != 'auth') or \
		(obj1._meta.app_label != 'auth' and obj2._meta.app_label == 'auth'):
			print "Rejecting cross-table relationship", obj1._meta.app_label, \
			obj2._meta.app_label
			return False
		return True

	def allow_migrate(self, db, app_label, model=None, **hints):
		return True
