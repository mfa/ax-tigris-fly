import io
import json
import os

import boto3
from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from .utils import check_signature

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


def save(dataset, uid=None):
    service = boto3.client("s3", endpoint_url="https://fly.storage.tigris.dev")

    buf = io.BytesIO()
    buf.write(json.dumps(dataset).encode())
    buf.seek(0)

    # upload "file" to S3
    bucket = os.environ.get("TIGRIS_BUCKET")
    # determine filename: uid parameter, uid field in data
    name = uid if uid else dataset.get("uid")
    service.upload_fileobj(buf, bucket, f"{name}.json")


@app.route("/", methods=["POST", "GET"])
async def home():
    if request.method == "GET":
        return "nothing to see here"
    else:
        uid = request.args.get("uid")
        data = request.data
        signature = request.headers.get("X-MYAX-SIGNATURE")
        secret = os.environ.get("AX_WEBHOOK_SECRET")
        if check_signature(signature, data, secret):
            print("signature valid")
            dataset = json.loads(data)
            if "id" in dataset:
                dataset["document_id"] = dataset.pop("id")
            save(dataset, uid)

    return "OK"
