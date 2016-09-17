```
sudo apt-get install git
git clone https://github.com/JesseAldridge/db_counter
cd db_counter
chmod +x install.sh run.sh
./install.sh
```

Make a `secrets.py` file following the example in `secrets.py.fake_example`.
Then you can do `./run.sh` and you should be able to view the data through your web browser.
