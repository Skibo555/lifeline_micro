import requests
import asyncio

INVALID_RES = {
    "status_code": "",
    "detail": ""
}

USER_SERVICES_URI = ""

def check_matches(users_details: list):
    req = requests.get(url=USER_SERVICES_URI, data=users_details)
    try:
        if req.status_code == 200:
            req_json = req.json()
            return req_json
        else:
            INVALID_RES["status_code"] = req.status_code
            INVALID_RES["detail"] = req
            raise INVALID_RES
    except Exception as ex:
        print(ex)
        return ex

