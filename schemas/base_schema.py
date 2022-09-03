

def serializeDict(a) -> dict:
    res = {}
    for i in a:
        if i == '_id':
            res[i] = str(a[i])
        else:
            res[i] = a[i]
    return res

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]
