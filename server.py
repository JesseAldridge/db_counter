import sys, glob, os, json, re

import flask


app = flask.Flask(__name__)
port = int(sys.argv[1]) if len(sys.argv) == 2 else 80

app.jinja_env.variable_start_string='{[{'
app.jinja_env.variable_end_string='}]}'

@app.route('/')
def index():
  lines = []
  for app_name in os.listdir('data'):
    if not os.path.isdir(os.path.join('data', app_name)):
      continue
    lines.append('<p><a href="/render_graphs/{}">{}</a></p>'.format(app_name, app_name))
  return '\n'.join([line for line in lines])


@app.route('/render_graphs/<app_name>')
def render_graphs(app_name):
  if not re.match('^[a-zA-Z0-9\-_]+$', app_name):
    return 'bad app name', 400

  render_list = [{'html': '<h2>{}</h2>'.format(app_name)}]
  for path in sorted(glob.glob(os.path.join('data', app_name, '*.txt'))):
    table_name = os.path.basename(path.rsplit('.', 1)[0])
    render_list.append({'html': '<h3>{}</h3>'.format(table_name)})

    with open(path) as f:
      text = f.read()
    dt_str_count_pairs =[]
    for line in text.splitlines():
      dt_str, count = line.rsplit(' ', 1)
      count = int(count)
      dt_str_count_pairs.append([dt_str, count])
    render_list.append({'points': [dt_str_count_pairs], 'show_lines': True})
  render_list_str = json.dumps(render_list)
  return flask.render_template('render_graphs.html', render_list=render_list_str)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port, debug=(port != 80))
