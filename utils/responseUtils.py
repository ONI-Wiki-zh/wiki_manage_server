def makeResponseJson(code, data=None, length=-1, msg=""):
    return {
        "code": code,
        "data": data,
        "length": length,
        "msg": msg
    }