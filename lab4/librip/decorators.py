def print_result(func_to_decorate):
    def decorated_func(*args):
        res = func_to_decorate(*args)
        print(func_to_decorate.__name__)
        if type(res) is str or type(res) is int:
            print(res)
        if type(res) is list:
            list(map(lambda x: print(x), res))
        if type(res) is dict:
            for k, v in res.items():
                print('{} = {}'.format(k, v))
        return res


    return decorated_func
