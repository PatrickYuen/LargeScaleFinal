class UserRouter(object):
  def _shard_num_by_user_id(self, user_id):
    print "Reading user %d" % user_id
    return user_id % 2; # for now just doing mod 2,  TODO!

  def db_for_read(self, model, **hints):
    """ """
    print model._meta.db_table
    if model._meta.db_table == 'auth_user':
      return "auth"
    if model._meta.db_table == 'micro_post':
      try:
        self._shard_num_by_user_id(hints['instance'].user_id)
      except KeyError:
        try:
          self._shard_num_by_user_id(int(hints['user_id']))
        except KeyError:
          print "No instance in hints. FIXME:fail"
    return None
  
  def db_for_write(self, model, **hints):
    return None

  def allow_relation(self, obj1, obj2, **hints):
    return True

  def allow_migrate(self, db, app_label, model=None, **hints):
    return True
