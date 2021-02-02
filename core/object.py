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

    ## **pytest callback**: remove hashes, id(self) from full tree dumps
    def test(self): return self.dump(test=True)

    ## @name IDump text dump for debug purposes

    ## **print callback**
    def __repr__(self): return self.dump()

    ## **full** text tree **dump**
    def dump(self, cycle=[], depth=0, prefix='', test=False):
        ret = self.pad(depth) + self.head(prefix, test)
        # block cycles
        if not depth:
            cycle = []
        if self in cycle:
            return ret + ' _/'
        else:
            cycle.append(self)
        # slot{}
        for i in sorted(self.slot.keys()):
            ret += self.slot[i].dump(cycle, depth + 1, f'{i} = ', test)
        for j, k in enumerate(iter(self)):
            ret += k.dump(cycle, depth + 1, f'{j} : ', test)
        return ret

    ## tree padding
    def pad(self, depth):
        return '\n' + '\t' * depth

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

    def json(self, depth=0):
        ret = '{'
        ret += f'"tag":"{self.tag()}","val":"{self.val()}"'
        ret += '}'
        return ret

    ## @name ICompiler code generation & source-to-source compilation

    ## @name IWeb generation for the web interface

    def html(self, request, depth=0):
        raise NotImplementedError(self.__class__, 'html', self)
