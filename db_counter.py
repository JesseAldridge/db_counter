import os, shutil, time, traceback
from datetime import datetime

import records

import secrets


def write_rotate(path, line):
  with open(path, 'a') as f:
   f.write(line)

  # limit files to 1 MB
  if os.path.getsize(path) > 1024 ** 2:
    shutil.move(path, path + '.old')

if not os.path.exists('data'):
  os.mkdir('data')

while True:
  try:
    for app_name, db_url_with_creds in secrets.app_db_tuples:
      print 'app_name:', app_name
      db = records.Database(db_url_with_creds)

      if not os.path.exists(os.path.join('data', app_name)):
        os.mkdir(os.path.join('data', app_name))

      query = 'SELECT * FROM pg_catalog.pg_tables'
      table_rows = db.query(query)

      for table_row in table_rows:
        table_name = table_row['tablename']
        if table_name.startswith('pg_') and table_name != 'pg_locks':
          continue
        if table_name.startswith('sql_'):
          continue

        print '  counting table rows: {}'.format(table_name)
        query = 'SELECT count(*) FROM {}'.format(table_name)
        rows = db.query(query)

        out_path = os.path.join('data', app_name, '{}.txt'.format(table_name))
        write_rotate(out_path, '{} {}\n'.format(datetime.utcnow(), rows[0]['count']))
  except Exception as e:
    line = u'exception: {}; {}'.format(type(e).__name__, e.message).encode('utf8')
    write_rotate('errors.txt', line)
    write_rotate('errors.txt', traceback.format_exc())
    time.sleep(10)
