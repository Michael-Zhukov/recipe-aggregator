import json


def process(f):
    file = open(f, encoding="utf-8")
    d = json.loads(file.read())
    res = []
    i = 0

    while i < len(d):
        item = d[i]
        if item["title"] != None and item["title"] != "":
            t = item["title"]
            t2 = ""
            for c in range(len(t)):
                t2 = t2 + t[c].lower()
            t2 = " ".join(t2.split())

            tm = 0
            try:
                tm = int(item["cooking_time"])
            except:
                tm = 0

            res.append([t2, item["category"], tm, item["main_ingredient"]])
        i = i + 1

    res2 = []
    for x in range(len(res)):
        found = False
        for y in range(len(res2)):
            if res2[y][0] == res[x][0] and res2[y][1] == res[x][1]:
                found = True
        if found == False:
            res2.append(res[x])

    st = {}
    for x in range(len(res2)):
        ingredient = res2[x][3]
        if ingredient in st.keys():
            st[ingredient] = st[ingredient] + 1
        else:
            st[ingredient] = 1

    print(st)
    return res2
