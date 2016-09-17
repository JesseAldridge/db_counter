rsync --exclude=".git" --exclude="junk" --exclude="data" -v -r . ubuntu@db-counter:~/db_counter
ssh db-counter
