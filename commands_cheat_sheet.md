## Useful Commands (Run it in your machine)

### Flask & Python
`virtualenv venv`
`source ./venv/bin/activate`
`deactivate`
`pip3 install -r requirements.txt`
`python3 ./app.py`

### Common commands needed for mongodb

#### Install on WSL
`sudo apt install mongodb`
`sudo service mongodb start`

#### Working w/ mongo itself

`sudo mongo`

```
show dbs
use <db_name>
show collections
db.<collection>.find(<optional_condition>)
```

### Common needed commands

#### Set python3 priorities

```
sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.7 2
sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 3

sudo update-alternatives --config python
```
> I'm using Python3.6 i guess

#### Kill open listening Ports on Windows

`netstat -a -n -o | findstr 5000`

`kill {PID}`

### Gmail SMTP 

[How to Authenticate with gmail smtp server](https://support.google.com/accounts/answer/185833?p=InvalidSecondFactor&visit_id=637782802776271348-3112394180&rd=1)

[Gmail apps password](myaccount.google.com/apppasswords)
