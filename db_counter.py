import os, shutil, time, traceback, subprocess
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
    for app_name in secrets.app_names:
      print 'app_name:', app_name
      proc = subprocess.Popen(
          'heroku config:get ALEMBIC_DATABASE_URL --app {}'.format(app_name).split(),
          stdout=subprocess.PIPE)
      _db_url_with_creds = proc.communicate()[0]
      db = records.Database(_db_url_with_creds)

      if not os.path.exists(os.path.join('data', app_name)):
        os.mkdir(os.path.join('data', app_name))

      query = 'SELECT * FROM pg_catalog.pg_tables'
      table_rows = db.query(query)

      def should_check_table(table_name):
        if table_name == 'pg_locks':
          return True
        return not(table_name.startswith('pg_') or table_name.startswith('sql_'))

      table_names = [table_row['tablename'] for table_row in table_rows if
                     should_check_table(table_row['tablename'])] + ['pg_locks']
      for table_name in table_names:
        if table_name.startswith('pg_') and table_name != 'pg_locks':
          continue
        if table_name.startswith('sql_'):
          continue

        print '  counting table rows: {}'.format(table_name)
        query = 'SELECT count(*) FROM {}'.format(table_name)
        rows = db.query(query)

        out_path = os.path.join('data', app_name, '{}.txt'.format(table_name))
        out_line = '{} {}\n'.format(datetime.utcnow(), rows[0]['count'])
        write_rotate(out_path, out_line)
  except Exception as e:
    line = u'exception: {}; {}'.format(type(e).__name__, e.message).encode('utf8')
    write_rotate('errors.txt', line)
    write_rotate('errors.txt', traceback.format_exc())
    time.sleep(10)
