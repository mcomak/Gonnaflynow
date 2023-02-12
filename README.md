# Installation

1. `git clone https://github.com/mcomak/web_scratching.git`
2. `python3 -m pip install virtualenv`
3. `cd gonnaflynow/`
4. `python3 -m virtualenv flyenv`
5. `source flyenv/bin/activate`
6. `pip install -r requirements.txt`

# Postgresql Commands

1. Check Status

`sudo systemctl status postgresql-10`

2. 
`psql -U train -d traindb`

3. show tables: `\dt`

4. `psql -U train -W -h localhost sky`


postgresql root authorization: 
`sudo -U postgres bash -c 'psql'` 

