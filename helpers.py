def get_child(place, places):
    subs = [subplace for subplace in places if subplace["parent"] == place["id"]]

    children = []

    for sub in subs:
        s = sub.copy()
        s["children"] = get_child(sub, places)
        children.append(s)

    return children
