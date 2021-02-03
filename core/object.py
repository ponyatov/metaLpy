## @file

## base graph node class / generic **code=data** & knowledge representation (AST/ASG)
## @ingroup core
class Object:

    ## named node constructor
    ## @param[in] V **node name** / other `Object` instance can be used as a prototype
    def __init__(self, V):
        if isinstance(V, Object):
            V = V.value
        ## node **class/type tag**
        self.type = self.__class__.__name__.lower()
        ## node name / **scalar value**
        self.value = V
        ## slot{}s / attributes / **associative array**
        self.slot = {}
        ## nest[]ed elements / **ordered container**
        self.nest = []

    ## @name ITest
    ## @ingroup test

    ## **pytest callback**: full tree dump for tests (without hashes/id/..)
    ## @ingroup test
    def test(self): return self.dump(test=True)

    ## @name IDump text dump for debug purposes

    ## **print callback**
    def __repr__(self): return self.dump()

    ## **full** text tree **dump**
    ## @param[in] cycle recursion block
    ## @param[in] depth recursion depth
    ## @param[in] prefix before `<T:V>` header /optional/
    ## @param[in] test use dump in tests (disable hashes/id/..)
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        # head
        ret = self.pad(depth) + self.head(prefix, test)
        # cycle
        if not depth: # init
            cycle = []
        if self in cycle:
            return ret + ' _/'
        else:
            cycle += [self]
        # slot{}
        for i in sorted(self.slot.keys()):
            ret += self.slot[i].dump(cycle, depth + 1, f'{i} = ', test)
        # nest[]
        for j, k in enumerate(iter(self)):
            ret += k.dump(cycle, depth + 1, f'{j} : ', test)
        return ret

    ## tree padding
    ## @param[in] depth tree depth = number of tabs
    ## @param[in] what to pad /optional/
    def pad(self, depth, what=''):
        return '\n' + '\t' * depth + f'{what}'

    ## **short** `<T:V>` header-only **dump**
    def head(self, prefix='', test=False):
        suffix = '' if test else f' @{id(self):x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{suffix}'

    ## dump `<T:` type (constant/reflection)
    def tag(self): return self.type

    ## dump `:V>` value (as string)
    def val(self): return f'{self.value}'

    ## @name IOperator operator redefinition & base operations over object graphs

    ## `if A`
    def __bool__(self): return bool(self.nest)

    ## `A.keys()` slot{} names /sorted/
    def keys(self):
        return sorted(self.slot.keys())

    ## `A.key`
    def __getattr__(self, key):
        assert isinstance(key, str)
        return self[key]

    ## `A[key]` get subgraph by name/index
    ## @param[in] key `slot{str:name}` or  `nest[int:index]`
    def __getitem__(self, key):
        if isinstance(key, str):
            return self.slot[key]
        if isinstance(key, int):
            return self.nest[key]
        raise TypeError(key, type(key))

    ## `A[key] = B` assign new slot
    ## @param[in] key slot name /string/
    ## @param[in] that subgraph to be assigned
    def __setitem__(self, key, that):
        assert isinstance(key, str)
        assert isinstance(that, Object)
        self.slot[key] = that
        return self

    ## `A[B.type] = B`
    def __lshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.type, that)

    ## `A[B.value] = B`
    def __rshift__(self, that):
        assert isinstance(that, Object)
        return self.__setitem__(that.value, that)

    ## `A // B` push subgraph into nest[]ed as a stack
    def __floordiv__(self, that):
        assert isinstance(that, Object)
        self.nest.append(that)
        return self

    ## `A.push(B)`
    def push(self, that): return self // that

    ## `A.pop`
    def pop(self): return self.nest.pop()

    ## iterator over nest[]ed
    def __iter__(self):
        for j in self.nest:
            yield j

    ## @name ISerialize multiformat (de)serialization for persistence & message passing
    ## @ingroup ser

    ## @ingroup ser
    ## @param[in] cycle recursion block
    ## @param[in] depth recursion depth
    ## @param[in] minify minification (else tabbed .json)
    def json(self, cycle=[], depth=0, minify=True):
        #
        assert self not in cycle
        #
        if minify:
            d0 = d1 = d2 = ''
        else:
            d0 = f'{self.pad(depth+0)}'
            d1 = f'{self.pad(depth+1)}'
            d2 = f'{self.pad(depth+2)}'
        # <head>
        ret = f'{d0}{{'
        ret += f'{d1}"tag":"{self.tag()}"'
        ret += f',{d1}"val":"{self.val()}"'
        # slot{}
        assert self.keys() == []
        # nest[]
        if self.nest:
            ret += f',{d1}"nest":['
            ret += ','.join(
                map(lambda j: j.json(cycle + [self], depth + 2, minify),
                    self.nest))
            ret += f'{d1}]'
        ret += f'{d0}}}'
        return ret

    ## @name ICompiler code generation & source-to-source compilation

    ## @name IWeb generation for the web interface
    ## @ingroup web

    ## represent as Socket.IO message
    ## @ingroup web
    ## @param[in] request web server request context
    ## @param[in] depth recursion depth
    def sio(self, request, depth=0):
        raise NotImplementedError(self.__class__, 'sio', self)

    ## represent as html code
    ## @ingroup web
    ## @param[in] request web server request context
    ## @param[in] depth recursion depth
    def html(self, request, depth=0):
        raise NotImplementedError(self.__class__, 'html', self)

    ## ajax/http GET
    ## @ingroup web
    ## @param[in] request web server request context
    ## @param[in] depth recursion depth
    def get(self, request, depth=0):
        raise NotImplementedError(self.__class__, 'get', self)

    ## ajax/http POST
    ## @ingroup web
    ## @param[in] request web server request context
    ## @param[in] depth recursion depth
    def post(self, request, depth=0):
        raise NotImplementedError(self.__class__, 'post', self)
