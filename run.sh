sudo killall gunicorn
python db_counter.py 2>&1 | python logrot/logrot.py db_counter_out.txt &
sudo gunicorn -w 4 server:app -b 0.0.0.0:80 --log-file=- | python logrot/logrot.py gunicorn_out.txt &
