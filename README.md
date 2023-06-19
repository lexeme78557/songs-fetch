# A Todo List demo App
This is a todo list demo designed for CS411. 
# Tutorial
<iframe width="560" height="315" src="https://www.youtube.com/embed/sY1lLGe7ECA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

A comprehensive writeup is avaliable [here](https://tichung.com/blog/2021/20200323_flask/).

## Requirements
```
python >= 3.5
xcrun command line tools
```

## Getting started

```bash
git clone https://github.com/lexeme78557/songs-fetch.git
cd songs-fetch
=python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install flask_cors
export FLASK_APP=app
flask run
```

## Setting up GCP
Create a `app.yaml` file in the root folder with the following content:
```yaml
runtime: python38 # or another supported version

instance_class: F1

env_variables:
  MYSQL_USER: <user_name> # please put in your credentials
  MYSQL_PASSWORD: <user_pw> # please put in your credentials
  MYSQL_DB: <database_name> # please put in your credentials
  MYSQL_HOST: <database_ip> # please put in your credentials

handlers:
# Matches requests to /images/... to files in static/images/...
- url: /img
  static_dir: static/img

- url: /script
  static_dir: static/script

- url: /styles
  static_dir: static/styles
```

Setting up the deployment
```bash
curl https://sdk.cloud.google.com | bash
gcloud components install app-engine-python
gcloud auth login
gcloud config set project core-site-365801
gcloud app deploy
```
