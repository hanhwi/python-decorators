import operator

class cacheable(object):
    ''' an applied function's args should be hashable '''
    def __init__(self, fn):
        self.table = {}
        self.fn = fn

    def __call__(self, *args, **kwargs):
        fn_para_names = self.fn.func_code.co_varnames
        key = [0 for x in range(0, self.fn.func_code.co_argcount)]
        keyset = [False for x in range(0, self.fn.func_code.co_argcount)]

        if self.fn.func_defaults:
            for i, v in enumerate(self.fn.func_defaults):
                rev_idx = -(i + 1)
                key[rev_idx] = v
                keyset[rev_idx] = True

        for i, v in enumerate(args):
            key[i] = v
            keyset[i] = True

        for v in kwargs:
            idx = fn_para_names.index(v)
            assert idx >= len(args)
            key[idx] = v
            keyset[idx] = True

        all_keys_set = reduce(operator.and_, keyset, True)
        assert all_keys_set
        
        key = tuple(key)
        if key in self.table:
            print "Key found", key
            return self.table[key]
        else:
            value = self.fn(*args, **kwargs)
            self.table[key] = value
            return value
