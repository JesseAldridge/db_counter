python db_counter.py 2>&1 | python logrot/logrot.py &
sudo gunicorn -w 4 server:app -b 0.0.0.0:80 --log-file=- &
