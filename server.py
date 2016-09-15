import sys, glob, os, json

import flask


app = flask.Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 80

app.jinja_env.variable_start_string='{[{'
app.jinja_env.variable_end_string='}]}'

@app.route('/')
def index():
  render_list = []
  for app_name in os.listdir('data'):
    if not os.path.isdir(os.path.join('data', app_name)):
      continue
    render_list.append({'html': '<h2>{}</h2>'.format(app_name)})
    for path in glob.glob(os.path.join('data', app_name, '*.txt')):
      table_name = os.path.basename(path.rsplit('.', 1)[0])
      render_list.append({'html': '<h3>{}</h3>'.format(table_name)})

      with open(path) as f:
        text = f.read()
      dt_str_count_pairs =[]
      for line in text.splitlines():
        dt_str, count = line.rsplit(' ', 1)
        count = int(count)
        dt_str_count_pairs.append([dt_str, count])
      render_list.append({'points': dt_str_count_pairs})

  return flask.render_template('index.html', render_list=json.dumps(render_list, indent=2))

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, debug=(port != 80))
