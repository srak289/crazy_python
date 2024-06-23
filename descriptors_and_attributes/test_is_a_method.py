from pathlib import Path
import pytest

class ismethod:
    '''
    Lets a function know whether it is being called as a method::

        class a: pass

        @ismethod
        def meth(self, *args, **kwargs):
            print('method' if self is not None else 'not method')
        a.meth = meth
        

        a.meth() # class method (so a method)

        a().meth() # method


        meth() # not a method

    '''
    def __init__(self, func):
        self._func = func
        self._obj = None
        self._cls = None

    def __get__(self, obj, cls):
        self._obj = obj
        self._cls = cls
        return self

    def __call__(self, *args, **kwargs):
        return self._func(self._obj if self._obj else self._cls, *args, **kwargs)

# Solution
#exec(Path('../solutions/test_is_a_method.py').read_text())

# validation tests

def test_not_method():
    @ismethod
    def fun(self, a, b):
        assert self is None
        return a*b
    assert fun(3,4) == 12
    with pytest.raises(TypeError):
        fun(4,5,5)

def test_as_method():
    class OurClass:

        @ismethod
        def meth_1(self, *args):
            return [self]*len(args)


    @ismethod
    def meth_2(self):
        return self

    assert meth_2() is None
    assert OurClass.meth_1(20,30) == [OurClass, OurClass]
    obj = OurClass()
    assert obj.meth_1(20) == [obj]
