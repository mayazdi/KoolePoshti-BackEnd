# KoolePoshti-BackEnd


## Useful Help

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