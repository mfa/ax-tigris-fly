import hashlib
import hmac


def check_signature(sig, data, secret):
    try:
        signature_header = sig.replace("sha1=", "")
        signature_content = hmac.new(
            key=secret.encode("utf-8"), msg=data, digestmod=hashlib.sha1
        ).hexdigest()
    except AttributeError:
        pass
    except KeyError:
        pass
    except Exception:
        raise
    else:
        return bool(signature_header == signature_content)
    return False
