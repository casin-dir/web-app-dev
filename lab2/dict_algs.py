ivan = {
    "name":"ivan",
    "age":34,
    "children":[{
        "name":"vasja",
        "age":15,
    },{
        "name":"petja",
        "age":10,
    }],
}
darja = {
    "name":"darja",
    "age":41,
    "children":[{
        "name":"kirill",
        "age":21,
    },{
        "name":"pavel",
        "age":19,
    }],
}
emps = [ivan, darja]

def print_emps_with_old_childrens(arr):
    for man in arr:
        for child in man.get('children'):
            if child.get('age') > 18:
                print(man.get('name'))
                break

if __name__ == "__main__":
    print_emps_with_old_childrens(emps)