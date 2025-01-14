# Meta Class

> 深刻理解python中的元类

[传送门](https://www.pythontab.com/html/2015/pythonhexinbiancheng_0906/961.html)

[StackOverflow](https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python)

[Stack Overflow About Python(中文)](https://www.bookstack.cn/read/stackoverflow-about-python/README.md)

## My Note

用关键字`class`定义的类也是一个对象，是一个可以创建对象的对象

`This object (the class) is itself capable of creating objects (the instances), and this is why it's a class.`

# Classes as objects

Before understanding metaclasses, you need to master classes in Python. And Python has a very peculiar idea of what classes are, borrowed from the Smalltalk language.

In most languages, classes are just pieces of code that describe how to produce an object. That's kinda true in Python too:

```py
>>> class ObjectCreator(object):
...       pass
...

>>> my_object = ObjectCreator()
>>> print(my_object)
<__main__.ObjectCreator object at 0x8974f2c>
```

But classes are more than that in Python. Classes are objects too.

Yes, objects.

As soon as you use the keyword `class`, Python executes it and creates an OBJECT. The instruction

```py
>>> class ObjectCreator(object):
...       pass
...
```

creates in memory an object with the name "ObjectCreator".

**This object (the class) is itself capable of creating objects (the instances), and this is why it's a class**.

But still, it's an object, and therefore:

- you can assign it to a variable
- you can copy it
- you can add attributes to it
- you can pass it as a function parameter

e.g.:

```py
>>> print(ObjectCreator) # you can print a class because it's an object
<class '__main__.ObjectCreator'>
>>> def echo(o):
...       print(o)
...
>>> echo(ObjectCreator) # you can pass a class as a parameter
<class '__main__.ObjectCreator'>
>>> print(hasattr(ObjectCreator, 'new_attribute'))
False
>>> ObjectCreator.new_attribute = 'foo' # you can add attributes to a class
>>> print(hasattr(ObjectCreator, 'new_attribute'))
True
>>> print(ObjectCreator.new_attribute)
foo
>>> ObjectCreatorMirror = ObjectCreator # you can assign a class to a variable
>>> print(ObjectCreatorMirror.new_attribute)
foo
>>> print(ObjectCreatorMirror())
<__main__.ObjectCreator object at 0x8997b4c>
```

# Creating classes dynamically

Since classes are objects, you can create them on the fly, like any object.

First, you can create a class in a function using `class`:

```py
>>> def choose_class(name):
...     if name == 'foo':
...         class Foo(object):
...             pass
...         return Foo # return the class, not an instance
...     else:
...         class Bar(object):
...             pass
...         return Bar
...
>>> MyClass = choose_class('foo')
>>> print(MyClass) # the function returns a class, not an instance
<class '__main__.Foo'>
>>> print(MyClass()) # you can create an object from this class
<__main__.Foo object at 0x89c6d4c>
```

But it's not so dynamic, since you still have to write the whole class yourself.

Since classes are objects, they must be generated by something.

When you use the `class` keyword, Python creates this object automatically. But as with most things in Python, it gives you a way to do it manually.

Remember the function `type`? The good old function that lets you know what type an object is:

```py
>>> print(type(1))
<type 'int'>
>>> print(type("1"))
<type 'str'>
>>> print(type(ObjectCreator))
<type 'type'>
>>> print(type(ObjectCreator()))
<class '__main__.ObjectCreator'>
```

Well, [`type`](http://docs.python.org/2/library/functions.html#type) has a completely different ability, it can also create classes on the fly. `type` can take the description of a class as parameters, and return a class.

(I know, it's silly that the same function can have two completely different uses according to the parameters you pass to it. It's an issue due to backward compatibility in Python)

`type` works this way:

```py
type(name, bases, attrs)
```

Where:

- **`name`**: name of the class
- **`bases`**: tuple of the parent class (for inheritance, can be empty)
- **`attrs`**: dictionary containing attributes names and values

e.g.:

```py
>>> class MyShinyClass(object):
...       pass
```

can be created manually this way:

```py
>>> MyShinyClass = type('MyShinyClass', (), {}) # returns a class object
>>> print(MyShinyClass)
<class '__main__.MyShinyClass'>
>>> print(MyShinyClass()) # create an instance with the class
<__main__.MyShinyClass object at 0x8997cec>
```

You'll notice that we use "MyShinyClass" as the name of the class and as the variable to hold the class reference. They can be different, but there is no reason to complicate things.

`type` accepts a dictionary to define the attributes of the class. So:

```py
>>> class Foo(object):
...       bar = True
```

Can be translated to:

```py
>>> Foo = type('Foo', (), {'bar':True})
```

And used as a normal class:

```py
>>> print(Foo)
<class '__main__.Foo'>
>>> print(Foo.bar)
True
>>> f = Foo()
>>> print(f)
<__main__.Foo object at 0x8a9b84c>
>>> print(f.bar)
True
```

And of course, you can inherit from it, so:

```py
>>>   class FooChild(Foo):
...         pass
```

would be:

```py
>>> FooChild = type('FooChild', (Foo,), {})
>>> print(FooChild)
<class '__main__.FooChild'>
>>> print(FooChild.bar) # bar is inherited from Foo
True
```

Eventually, you'll want to add methods to your class. Just define a function with the proper signature and assign it as an attribute.

```py
>>> def echo_bar(self):
...       print(self.bar)
...
>>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
>>> hasattr(Foo, 'echo_bar')
False
>>> hasattr(FooChild, 'echo_bar')
True
>>> my_foo = FooChild()
>>> my_foo.echo_bar()
True
```

And you can add even more methods after you dynamically create the class, just like adding methods to a normally created class object.

```py
>>> def echo_bar_more(self):
...       print('yet another method')
...
>>> FooChild.echo_bar_more = echo_bar_more
>>> hasattr(FooChild, 'echo_bar_more')
True
```

You see where we are going: in Python, classes are objects, and you can create a class on the fly, dynamically.

This is what Python does when you use the keyword `class`, and it does so by using a metaclass.

# What are metaclasses (finally)

Metaclasses are the 'stuff' that creates classes.

You define classes in order to create objects, right?

But we learned that Python classes are objects.

Well, metaclasses are what create these objects. They are the classes' classes, you can picture them this way:

```py
MyClass = MetaClass()
my_object = MyClass()
```

You've seen that `type` lets you do something like this:

```py
MyClass = type('MyClass', (), {})
```

It's because the function `type` is in fact a metaclass. `type` is the metaclass Python uses to create all classes behind the scenes.

Now you wonder why the heck is it written in lowercase, and not `Type`?

Well, I guess it's a matter of consistency with `str`, the class that creates strings objects, and `int` the class that creates integer objects. `type` is just the class that creates class objects.

You see that by checking the `__class__` attribute.

Everything, and I mean everything, is an object in Python. That includes ints, strings, functions and classes. All of them are objects. And all of them have been created from a class:

```py
>>> age = 35
>>> age.__class__
<type 'int'>
>>> name = 'bob'
>>> name.__class__
<type 'str'>
>>> def foo(): pass
>>> foo.__class__
<type 'function'>
>>> class Bar(object): pass
>>> b = Bar()
>>> b.__class__
<class '__main__.Bar'>
```

Now, what is the `__class__` of any `__class__` ?

```py
>>> age.__class__.__class__
<type 'type'>
>>> name.__class__.__class__
<type 'type'>
>>> foo.__class__.__class__
<type 'type'>
>>> b.__class__.__class__
<type 'type'>
```

So, a metaclass is just the stuff that creates class objects.

You can call it a 'class factory' if you wish.

`type` is the built-in metaclass Python uses, but of course, you can create your own metaclass.

# The [`__metaclass__`](http://docs.python.org/2/reference/datamodel.html?highlight=__metaclass__#__metaclass__) attribute

In Python 2, you can add a `__metaclass__` attribute when you write a class (see next section for the Python 3 syntax):

```py
class Foo(object):
    __metaclass__ = something...
    [...]
```

If you do so, Python will use the metaclass to create the class `Foo`.

Careful, it's tricky.

You write `class Foo(object)` first, but the class object `Foo` is not created in memory yet.

Python will look for `__metaclass__` in the class definition. If it finds it, it will use it to create the object class `Foo`. If it doesn't, it will use `type` to create the class.

Read that several times.

When you do:

```py
class Foo(Bar):
    pass
```

Python does the following:

Is there a `__metaclass__` attribute in `Foo`?

If yes, create in-memory a class object (I said a class object, stay with me here), with the name `Foo` by using what is in `__metaclass__`.

If Python can't find `__metaclass__`, it will look for a `__metaclass__` at the MODULE level, and try to do the same (but only for classes that don't inherit anything, basically old-style classes).

Then if it can't find any `__metaclass__` at all, it will use the `Bar`'s (the first parent) own metaclass (which might be the default `type`) to create the class object.

Be careful here that the `__metaclass__` attribute will not be inherited, the metaclass of the parent (`Bar.__class__`) will be. If `Bar` used a `__metaclass__` attribute that created `Bar` with `type()` (and not `type.__new__()`), the subclasses will not inherit that behavior.

Now the big question is, what can you put in `__metaclass__`?

The answer is something that can create a class.

And what can create a class? `type`, or anything that subclasses or uses it.

# Metaclasses in Python 3

The syntax to set the metaclass has been changed in Python 3:

```py
class Foo(object, metaclass=something):
    ...
```

i.e. the `__metaclass__` attribute is no longer used, in favor of a keyword argument in the list of base classes.

The behavior of metaclasses however stays [largely the same](https://www.python.org/dev/peps/pep-3115/).

One thing added to metaclasses in Python 3 is that you can also pass attributes as keyword-arguments into a metaclass, like so:

```py
class Foo(object, metaclass=something, kwarg1=value1, kwarg2=value2):
    ...
```

Read the section below for how python handles this.

# Custom metaclasses

The main purpose of a metaclass is to change the class automatically, when it's created.

You usually do this for APIs, where you want to create classes matching the current context.

Imagine a stupid example, where you decide that all classes in your module should have their attributes written in uppercase. There are several ways to do this, but one way is to set `__metaclass__` at the module level.

This way, all classes of this module will be created using this metaclass, and we just have to tell the metaclass to turn all attributes to uppercase.

Luckily, `__metaclass__` can actually be any callable, it doesn't need to be a formal class (I know, something with 'class' in its name doesn't need to be a class, go figure... but it's helpful).

So we will start with a simple example, by using a function.

```py
# the metaclass will automatically get passed the same argument
# that you usually pass to `type`
def upper_attr(future_class_name, future_class_parents, future_class_attrs):
    """
      Return a class object, with the list of its attribute turned
      into uppercase.
    """
    # pick up any attribute that doesn't start with '__' and uppercase it
    uppercase_attrs = {
        attr if attr.startswith("__") else attr.upper(): v
        for attr, v in future_class_attrs.items()
    }

    # let `type` do the class creation
    return type(future_class_name, future_class_parents, uppercase_attrs)

__metaclass__ = upper_attr # this will affect all classes in the module

class Foo(): # global __metaclass__ won't work with "object" though
    # but we can define __metaclass__ here instead to affect only this class
    # and this will work with "object" children
    bar = 'bip'
```

Let's check:

```py
>>> hasattr(Foo, 'bar')
False
>>> hasattr(Foo, 'BAR')
True
>>> Foo.BAR
'bip'
```

Now, let's do exactly the same, but using a real class for a metaclass:

```py
# remember that `type` is actually a class like `str` and `int`
# so you can inherit from it
class UpperAttrMetaclass(type):
    # __new__ is the method called before __init__
    # it's the method that creates the object and returns it
    # while __init__ just initializes the object passed as parameter
    # you rarely use __new__, except when you want to control how the object
    # is created.
    # here the created object is the class, and we want to customize it
    # so we override __new__
    # you can do some stuff in __init__ too if you wish
    # some advanced use involves overriding __call__ as well, but we won't
    # see this
    def __new__(upperattr_metaclass, future_class_name,
                future_class_parents, future_class_attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in future_class_attrs.items()
        }
        return type(future_class_name, future_class_parents, uppercase_attrs)
```

Let's rewrite the above, but with shorter and more realistic variable names now that we know what they mean:

```py
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return type(clsname, bases, uppercase_attrs)
```

You may have noticed the extra argument `cls`. There is nothing special about it: `__new__` always receives the class it's defined in, as the first parameter. Just like you have `self` for ordinary methods which receive the instance as the first parameter, or the defining class for class methods.

But this is not proper OOP. We are calling `type` directly and we aren't overriding or calling the parent's `__new__`. Let's do that instead:

```py
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return type.__new__(cls, clsname, bases, uppercase_attrs)
```

We can make it even cleaner by using `super`, which will ease inheritance (because yes, you can have metaclasses, inheriting from metaclasses, inheriting from type):

```py
class UpperAttrMetaclass(type):
    def __new__(cls, clsname, bases, attrs):
        uppercase_attrs = {
            attr if attr.startswith("__") else attr.upper(): v
            for attr, v in attrs.items()
        }
        return super(UpperAttrMetaclass, cls).__new__(
            cls, clsname, bases, uppercase_attrs)
```

Oh, and in python 3 if you do this call with keyword arguments, like this:

```py
class Foo(object, metaclass=MyMetaclass, kwarg1=value1):
    ...
```

It translates to this in the metaclass to use it:

```py
class MyMetaclass(type):
    def __new__(cls, clsname, bases, dct, kwargs1=default):
        ...
```

That's it. There is really nothing more about metaclasses.

The reason behind the complexity of the code using metaclasses is not because of metaclasses, it's because you usually use metaclasses to do twisted stuff relying on introspection, manipulating inheritance, vars such as `__dict__`, etc.

Indeed, metaclasses are especially useful to do black magic, and therefore complicated stuff. But by themselves, they are simple:

- intercept a class creation
- modify the class
- return the modified class

# Why would you use metaclasses classes instead of functions?

Since `__metaclass__` can accept any callable, why would you use a class since it's obviously more complicated?

There are several reasons to do so:

- The intention is clear. When you read `UpperAttrMetaclass(type)`, you know what's going to follow
- You can use OOP. Metaclass can inherit from metaclass, override parent methods. Metaclasses can even use metaclasses.
- Subclasses of a class will be instances of its metaclass if you specified a metaclass-class, but not with a metaclass-function.
- You can structure your code better. You never use metaclasses for something as trivial as the above example. It's usually for something complicated. Having the ability to make several methods and group them in one class is very useful to make the code easier to read.
- You can hook on `__new__`, `__init__` and `__call__`. Which will allow you to do different stuff, Even if usually you can do it all in `__new__`, some people are just more comfortable using `__init__`.
- These are called metaclasses, damn it! It must mean something!

# Why would you use metaclasses?

Now the big question. Why would you use some obscure error-prone feature?

Well, usually you don't:

> Metaclasses are deeper magic that 99% of users should never worry about it. If you wonder whether you need them, you don't (the people who actually need them to know with certainty that they need them and don't need an explanation about why).

*Python Guru Tim Peters*

The main use case for a metaclass is creating an API. A typical example of this is the Django ORM. It allows you to define something like this:

```py
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

But if you do this:

```py
person = Person(name='bob', age='35')
print(person.age)
```

It won't return an `IntegerField` object. It will return an `int`, and can even take it directly from the database.

This is possible because `models.Model` defines `__metaclass__` and it uses some magic that will turn the `Person` you just defined with simple statements into a complex hook to a database field.

Django makes something complex look simple by exposing a simple API and using metaclasses, recreating code from this API to do the real job behind the scenes.

# The last word

First, you know that classes are objects that can create instances.

Well, in fact, classes are themselves instances. Of metaclasses.

```py
>>> class Foo(object): pass
>>> id(Foo)
142630324
```

Everything is an object in Python, and they are all either instance of classes or instances of metaclasses.

Except for `type`.

`type` is actually its own metaclass. This is not something you could reproduce in pure Python, and is done by cheating a little bit at the implementation level.

Secondly, metaclasses are complicated. You may not want to use them for very simple class alterations. You can change classes by using two different techniques:

- [monkey patching](http://en.wikipedia.org/wiki/Monkey_patch)
- class decorators

99% of the time you need class alteration, you are better off using these.

But 98% of the time, you don't need class alteration at all.



译注：这是一篇在Stack overflow上很热的帖子。提问者自称已经掌握了有关Python OOP编程中的各种概念，但始终觉得元类(metaclass)难以理解。他知道这肯定和自省有关，但仍然觉得不太明白，希望大家可以给出一些实际的例子和代码片段以帮助理解，以及在什么情况下需要进行元编程。于是e-satis同学给出了神一般的回复，该回复获得了985点的赞同点数，更有人评论说这段回复应该加入到Python的官方文档中去。而e-satis同学本人在Stack Overflow中的声望积分也高达64271分。以下就是这篇精彩的回复（提示：非常长）

# 类也是对象

在理解元类之前，你需要先掌握Python中的类。Python中类的概念借鉴于Smalltalk，这显得有些奇特。在大多数编程语言中，类就是一组用来描述如何生成一个对象的代码段。在Python中这一点仍然成立：

```
>>> class ObjectCreator(object):
…       pass
…
>>> my_object = ObjectCreator()
>>> print my_object
```

<__main__.objectcreator object="" at="" 0x8974f2c="">

但是，Python中的类还远不止如此。类同样也是一种对象。是的，没错，就是对象。只要你使用关键字class，Python解释器在执行的时候就会创建一个对象。下面的代码段：

```
>>> class ObjectCreator(object):
…       pass
…
```

将在内存中创建一个对象，名字就是ObjectCreator。这个对象（类）自身拥有创建对象（类实例）的能力，而这就是为什么它是一个类的原因。但是，它的本质仍然是一个对象，于是乎你可以对它做如下的操作：

1)  你可以将它赋值给一个变量

2)  你可以拷贝它

3)  你可以为它增加属性

4)  你可以将它作为函数参数进行传递

下面是示例：

```
>>> print ObjectCreator     
# 你可以打印一个类，因为它其实也是一个对象
>>> def echo(o):
…       print o
…
>>> echo(ObjectCreator)
            
# 你可以将类做为参数传给函数
>>> print hasattr(ObjectCreator, 'new_attribute')
Fasle
>>> ObjectCreator.new_attribute = 'foo' 
#  你可以为类增加属性
>>> print hasattr(ObjectCreator, 'new_attribute')
True
>>> print ObjectCreator.new_attribute
foo
>>> ObjectCreatorMirror = ObjectCreator 
# 你可以将类赋值给一个变量
>>> print ObjectCreatorMirror()
<__main__.objectcreator object="" at="" 0x8997b4c="">
```

# 动态地创建类

因为类也是对象，你可以在运行时动态的创建它们，就像其他任何对象一样。首先，你可以在函数中创建类，使用class关键字即可。

```
>>> def choose_class(name):
…       if name == 'foo':
…           class Foo(object):
…               pass
…           return Foo     
# 返回的是类，不是类的实例
…       else:
…           class Bar(object):
…               pass
…           return Bar
…
>>> MyClass = choose_class('foo')
>>> print MyClass              
# 函数返回的是类，不是类的实例>>> print MyClass()            
# 你可以通过这个类创建类实例，也就是对象
<__main__.foo object="" at="" 0x89c6d4c="">
```

但这还不够动态，因为你仍然需要自己编写整个类的代码。由于类也是对象，所以它们必须是通过什么东西来生成的才对。当你使用class关键字时，Python解释器自动创建这个对象。但就和Python中的大多数事情一样，Python仍然提供给你手动处理的方法。还记得内建函数type吗？这个古老但强大的函数能够让你知道一个对象的类型是什么，就像这样：

```
>>> print type(1)
>>> print type("1")
>>> print type(ObjectCreator)
>>> print type(ObjectCreator())
```



这里，type有一种完全不同的能力，它也能动态的创建类。type可以接受一个类的描述作为参数，然后返回一个类。（我知道，根据传入参数的不同，同一个函数拥有两种完全不同的用法是一件很傻的事情，但这在Python中是为了保持向后兼容性）

type可以像这样工作：

type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)

比如下面的代码：

```
>>> class MyShinyClass(object):
…       pass
```

可以手动像这样创建：

```
>>> MyShinyClass = type('MyShinyClass', (), {})  
# 返回一个类对象
>>> print MyShinyClass
>>> print MyShinyClass()  
#  创建一个该类的实例
<__main__.myshinyclass object="" at="" 0x8997cec="">
```

你会发现我们使用“MyShinyClass”作为类名，并且也可以把它当做一个变量来作为类的引用。类和变量是不同的，这里没有任何理由把事情弄的复杂。

type 接受一个字典来为类定义属性，因此

```
>>> class Foo(object):
…       bar = True
```

可以翻译为：

```
>>> Foo = type('Foo', (), {'bar':True})
```

并且可以将Foo当成一个普通的类一样使用：

```
>>> print Foo
>>> print Foo.bar
True
>>> f = Foo()
>>> print f
<__main__.foo object="" at="" 0x8a9b84c="">
>>> print f.bar
True
```

当然，你可以向这个类继承，所以，如下的代码：

```
>>> class FooChild(Foo):
…       pass
```

就可以写成：

```
>>> FooChild = type('FooChild', (Foo,),{})
>>> print FooChild
>>> print FooChild.bar   
# bar属性是由Foo继承而来
True
```

最终你会希望为你的类增加方法。只需要定义一个有着恰当签名的函数并将其作为属性赋值就可以了。

```
>>> def echo_bar(self):
…       print self.bar
…
>>> FooChild = type('FooChild', (Foo,), {'echo_bar': echo_bar})
>>> hasattr(Foo, 'echo_bar')
False
>>> hasattr(FooChild, 'echo_bar')
True
>>> my_foo = FooChild()
>>> my_foo.echo_bar()
True
```

你可以看到，在Python中，类也是对象，你可以动态的创建类。这就是当你使用关键字class时Python在幕后做的事情，而这就是通过元类来实现的。

 

# 到底什么是元类（终于到主题了）

元类就是用来创建类的“东西”。你创建类就是为了创建类的实例对象，不是吗？但是我们已经学习到了Python中的类也是对象。好吧，元类就是用来创建这些类（对象）的，元类就是类的类，你可以这样理解 为：

```
MyClass = MetaClass()
MyObject = MyClass()
```

你已经看到了type可以让你像这样做：

```
MyClass = type('MyClass', (), {})
```

这是因为函数type实际上是一个元类。type就是Python在背后用来创建所有类的元类。现在你想知道那为什么type会全部采用小写形式而不是Type呢？好吧，我猜这是为了和str保持一致性，str是用来创建字符串对象的类，而int是用来创建整数对象的类。type就是创建类对象的类。你可以通过检查__class__属性来看到这一点。Python中所有的东西，注意，我是指所有的东西——都是对象。这包括整数、字符串、函数以及类。它们全部都是对象，而且它们都是从一个类创建而来。

```
>>> age = 35
>>> age.__class__
>>> name = 'bob'
>>> name.__class__
>>> def foo(): pass
>>>foo.__class__
>>> class Bar(object): pass
>>> b = Bar()
>>> b.__class__
```



现在，对于任何一个__class__的__class__属性又是什么呢？

```
>>> a.__class__.__class__
>>> age.__class__.__class__
>>> foo.__class__.__class__
>>> b.__class__.__class__
```



因此，元类就是创建类这种对象的东西。如果你喜欢的话，可以把元类称为“类工厂”（不要和工厂类搞混了:D） type就是Python的内建元类，当然了，你也可以创建自己的元类。

 

# __metaclass__属性

你可以在写一个类的时候为其添加__metaclass__属性。

```
class Foo(object):
    __metaclass__ = something…
[…]
```

如果你这么做了，Python就会用元类来创建类Foo。小心点，这里面有些技巧。你首先写下class Foo(object)，但是类对象Foo还没有在内存中创建。Python会在类的定义中寻找__metaclass__属性，如果找到了，Python就会用它来创建类Foo，如果没有找到，就会用内建的type来创建这个类。把下面这段话反复读几次。当你写如下代码时 :

class Foo(Bar):

  pass

Python做了如下的操作：

Foo中有__metaclass__这个属性吗？如果是，Python会在内存中通过__metaclass__创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）。如果Python没有找到__metaclass__，它会继续在Bar（父类）中寻找__metaclass__属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到__metaclass__，它就会在模块层次中去寻找__metaclass__，并尝试做同样的操作。如果还是找不到__metaclass__,Python就会用内置的type来创建这个类对象。

现在的问题就是，你可以在__metaclass__中放置些什么代码呢？答案就是：可以创建一个类的东西。那么什么可以用来创建一个类呢？type，或者任何使用到type或者子类化type的东东都可以。

 

### 自定义元类

元类的主要目的就是为了当创建类时能够自动地改变类。通常，你会为API做这样的事情，你希望可以创建符合当前上下文的类。假想一个很傻的例子，你决定在你的模块里所有的类的属性都应该是大写形式。有好几种方法可以办到，但其中一种就是通过在模块级别设定__metaclass__。采用这种方法，这个模块中的所有类都会通过这个元类来创建，我们只需要告诉元类把所有的属性都改成大写形式就万事大吉了。

幸运的是，__metaclass__实际上可以被任意调用，它并不需要是一个正式的类（我知道，某些名字里带有‘class’的东西并不需要是一个class，画画图理解下，这很有帮助）。所以，我们这里就先以一个简单的函数作为例子开始。

\# 元类会自动将你通常传给‘type’的参数作为自己的参数传入

```
def upper_attr(future_class_name, future_class_parents, future_class_attr):
    
'''返回一个类对象，将属性都转为大写形式'''
    
#  选择所有不以'__'开头的属性
    attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
    
# 将它们转为大写形式
    uppercase_attr = dict((name.upper(), value) for name, value in attrs)
 
    
# 通过'type'来做类对象的创建
    return type(future_class_name, future_class_parents, uppercase_attr)
 
__metaclass__ = upper_attr  
#  这会作用到这个模块中的所有类
 
class Foo(object):
    
# 我们也可以只在这里定义__metaclass__，这样就只会作用于这个类中
    bar = 'bip'
print hasattr(Foo, 'bar')
# 输出: False
print hasattr(Foo, 'BAR')
# 输出:True
 
f = Foo()
print f.BAR
# 输出:'bip'
```

现在让我们再做一次，这一次用一个真正的class来当做元类。

```
# 请记住，'type'实际上是一个类，就像'str'和'int'一样
# 所以，你可以从type继承
class UpperAttrMetaClass(type):
    
# __new__ 是在__init__之前被调用的特殊方法
    
# __new__是用来创建对象并返回之的方法
    
# 而__init__只是用来将传入的参数初始化给对象
    
# 你很少用到__new__，除非你希望能够控制对象的创建
    
# 这里，创建的对象是类，我们希望能够自定义它，所以我们这里改写__new__
    
# 如果你希望的话，你也可以在__init__中做些事情
    
# 还有一些高级的用法会涉及到改写__call__特殊方法，但是我们这里不用
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return type(future_class_name, future_class_parents, uppercase_attr)
但是，这种方式其实不是OOP。我们直接调用了type，而且我们没有改写父类的__new__方法。现在让我们这样去处理:
class UpperAttrMetaclass(type):
    def __new__(upperattr_metaclass, future_class_name, future_class_parents, future_class_attr):
        attrs = ((name, value) for name, value in future_class_attr.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
 
        
# 复用type.__new__方法
        
# 这就是基本的OOP编程，没什么魔法
        return type.__new__(upperattr_metaclass, future_class_name, future_class_parents, uppercase_attr)
```

你可能已经注意到了有个额外的参数upperattr_metaclass，这并没有什么特别的。类方法的第一个参数总是表示当前的实例，就像在普通的类方法中的self参数一样。当然了，为了清晰起见，这里的名字我起的比较长。但是就像self一样，所有的参数都有它们的传统名称。因此，在真实的产品代码中一个元类应该是像这样的：

```
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__')
        uppercase_attr  = dict((name.upper(), value) for name, value in attrs)
        return type.__new__(cls, name, bases, uppercase_attr)
如果使用super方法的话，我们还可以使它变得更清晰一些，这会缓解继承（是的，你可以拥有元类，从元类继承，从type继承）
class UpperAttrMetaclass(type):
    def __new__(cls, name, bases, dct):
        attrs = ((name, value) for name, value in dct.items() if not name.startswith('__'))
        uppercase_attr = dict((name.upper(), value) for name, value in attrs)
        return super(UpperAttrMetaclass, cls).__new__(cls, name, bases, uppercase_attr)
```

就是这样，除此之外，关于元类真的没有别的可说的了。使用到元类的代码比较复杂，这背后的原因倒并不是因为元类本身，而是因为你通常会使用元类去做一些晦涩的事情，依赖于自省，控制继承等等。确实，用元类来搞些“黑暗魔法”是特别有用的，因而会搞出些复杂的东西来。但就元类本身而言，它们其实是很简单的：

1)  拦截类的创建

2)  修改类

3)  返回修改之后的类

 

为什么要用metaclass类而不是函数?

由于__metaclass__可以接受任何可调用的对象，那为何还要使用类呢，因为很显然使用类会更加复杂啊？这里有好几个原因：

1）  意图会更加清晰。当你读到UpperAttrMetaclass(type)时，你知道接下来要发生什么。

2） 你可以使用OOP编程。元类可以从元类中继承而来，改写父类的方法。元类甚至还可以使用元类。

3）  你可以把代码组织的更好。当你使用元类的时候肯定不会是像我上面举的这种简单场景，通常都是针对比较复杂的问题。将多个方法归总到一个类中会很有帮助，也会使得代码更容易阅读。

4） 你可以使用__new__, __init__以及__call__这样的特殊方法。它们能帮你处理不同的任务。就算通常你可以把所有的东西都在__new__里处理掉，有些人还是觉得用__init__更舒服些。

5） 哇哦，这东西的名字是metaclass，肯定非善类，我要小心！

 

究竟为什么要使用元类？

现在回到我们的大主题上来，究竟是为什么你会去使用这样一种容易出错且晦涩的特性？好吧，一般来说，你根本就用不上它：

“元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。”  —— Python界的领袖 Tim Peters

元类的主要用途是创建API。一个典型的例子是Django ORM。它允许你像这样定义：

```
class Person(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
```

但是如果你像这样做的话：

```
guy  = Person(name='bob', age='35')
print guy.age
```

这并不会返回一个IntegerField对象，而是会返回一个int，甚至可以直接从数据库中取出数据。这是有可能的，因为models.Model定义了__metaclass__， 并且使用了一些魔法能够将你刚刚定义的简单的Person类转变成对数据库的一个复杂hook。Django框架将这些看起来很复杂的东西通过暴露出一个简单的使用元类的API将其化简，通过这个API重新创建代码，在背后完成真正的工作。

 

结语

首先，你知道了类其实是能够创建出类实例的对象。好吧，事实上，类本身也是实例，当然，它们是元类的实例。

```
>>>class Foo(object): pass
>>> id(Foo)
```

Python中的一切都是对象，它们要么是类的实例，要么是元类的实例，除了type。type实际上是它自己的元类，在纯Python环境中这可不是你能够做到的，这是通过在实现层面耍一些小手段做到的。其次，元类是很复杂的。对于非常简单的类，你可能不希望通过使用元类来对类做修改。你可以通过其他两种技术来修改类：

1） Monkey patching

2)  class decorators

当你需要动态修改类时，99%的时间里你最好使用上面这两种技术。当然了，其实在99%的时间里你根本就不需要动态修改类 :D



