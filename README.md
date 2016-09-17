```
sudo apt-get install git
git clone https://github.com/JesseAldridge/db_counter
cd db_counter
./install.sh
```

Modify `secrets.py` to contain your application name and database login urls.  
Then you can do `./run.sh` and you should be able to view the data through your web browser.
Look at ~/logrot_out.txt for stdout/stderr for debugging.
