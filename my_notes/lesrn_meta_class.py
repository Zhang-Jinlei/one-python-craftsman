class ObjectCreator(object):
    pass


my_object = ObjectCreator()
print(my_object)
print(ObjectCreator)


def echo(o):
    print(o)


echo(ObjectCreator)
print(hasattr(ObjectCreator, 'new_attr'))
ObjectCreator.new_attr = 'foo'
print(hasattr(ObjectCreator, 'new_attr'))
print(ObjectCreator.new_attr)
ObjectCreatorMirror = ObjectCreator
print(ObjectCreatorMirror.new_attr)
print(ObjectCreatorMirror())


def choose_class(name):
    if name == 'foo':
        class Foo:
            pass

        return Foo
    else:
        class Bar:
            pass

        return Bar


MyClass = choose_class('foo')
print(MyClass)
print(MyClass())

