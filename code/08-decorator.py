#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-6-22 9:17
# @Author   : Jinlei
# @Describe ：
class Foo:
    def __call__(self):
        print("Hello, __call___")


foo = Foo()

# OUTPUT: True
print(callable(foo))
# 调用 foo 实例
# OUTPUT: Hello, __call__
foo()
