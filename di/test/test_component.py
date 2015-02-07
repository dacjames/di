import pytest

from di import inject, InjectionError


def test_smoke():

    def Bar():
        pass

    @inject(Bar)
    def Foo(bar):
        pass


def test_wrapping():

    def Bar():
        pass

    @inject()
    def Foo(bar):
        pass

    assert Foo.__name__ == 'Foo'
    assert Bar.__name__ == 'Bar'


def test_one_to_one():
    def Bar():
        return "hello, world"

    @inject(Bar)
    def Foo(bar):
        assert bar == "hello, world"

    foo = Foo()


def test_one_to_many():
    def Bar():
        return "hello, world"

    @inject(Bar)
    def Foo(bar):
        assert bar == "hello, world"

    @inject(Bar)
    def Qua(bar):
        assert bar == "hello, world"

    f = Foo()
    q = Qua()


def test_chain():
    def Bar():
        return "hello, world"

    @inject(Bar)
    def Foo(bar):
        assert bar == "hello, world"
        return bar[::-1]

    @inject(Foo)
    def Qua(foo):
        assert foo == "dlrow ,olleh"

    q = Qua()


def test_only_create_once():
    state = [0]

    def Bar():
        state[0] = state[0] + 1
        return "hello, world"

    @inject(Bar)
    def Foo(bar):
        assert bar == "hello, world"

    @inject(Bar)
    def Qua(bar):
        assert bar == "hello, world"

    assert state[0] == 0

    q = Qua()
    f = Foo()

    assert state[0] == 1


def test_invalid_injections():

    def Bar(x):
        return "hello"

    with pytest.raises(InjectionError) as e:
        @inject(Bar)
        def Foo(bar):
            return "world"

    assert "Bar" in str(e)
    assert "Foo" in str(e)
