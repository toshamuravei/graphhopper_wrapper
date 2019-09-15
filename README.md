# GraphHopper Wrapper

## Installation & configuration without Docker:
```sh
$ git clone https://github.com/toshamuravei/graphhopper_wrapper.git
$ cd graphhopper_wraper
$ virtualenv .env -p python3.7
$ source .env/bin/activate
$ pip install -r requirements.txt
$ cat >> graphhopper_wraper/settings/local.py
$ gunicorn -c config.py wsgi
```

## Installation & configuration with Docker:
```sh
$ git clone https://github.com/toshamuravei/graphhopper_wrapper.git
$ cd graphhopper_wraper
$ make build
$ make run_advanced
```
