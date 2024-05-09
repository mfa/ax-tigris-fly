## ax-tigris (fly.io)

store the webhook from AX in an S3 bucket (Tigris flavour)

this demo uses Flask and is deployed on fly.io


### setup

launch app
```
fly launch
```

scale down to one app which is enough for this demo
```
fly scale count 1
```

Create an s3 bucket. This sets automatically the secrets needed for S3 compatible access.
```
fly storage create -n ax-s3-demo
```

Set the webhook secret from AX:
```
flyctl secrets set AX_WEBHOOK_SECRET=copy-from-collection-settings-and-set-url-too
```

### development

in a virtualenv
```
python -m pip install -r requirements.txt
FLASK_APP=app.main flask run
```
