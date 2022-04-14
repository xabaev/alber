def ordering(obj):
    if isinstance(obj, dict):
        return sorted((k, ordering(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordering(x) for x in obj)
    else:
        return obj
