import os, sys, requests


def token(req):
    if "Authorization" not in req.headers:
        return None, ("Missing Credentials", 401)

    token = req.headers["Authorization"]

    if not token:
        return None, ("Missing Credentials", 401)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )
    print(response)
    if response.status_code == 200:
        print(response)
        return response.text, None

    else:
        return None, (response.text, response.status_code)
