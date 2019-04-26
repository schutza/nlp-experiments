def timefunc(f):
    def f_timer(*args, **kwargs):
        import time
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f'{f.__name__} took [{end - start}] seconds')
        return result
    return f_timer
