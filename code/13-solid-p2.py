#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021-6-21 14:31
# @Author   : Jinlei
# @Describe ：
class User:
    """普通用户模型类
    """

    def __init__(self, username: str):
        self.username = username

    def deactivate(self):
        """停用当前用户
        """
        self.is_active = False
        # self.save()


class Admin(User):
    """管理员用户类
    """

    def deactivate(self):
        # 管理员用户不允许被停用
        raise RuntimeError('admin can not be deactivated!')


def deactivate_users(users):
    """批量停用多个用户
    """
    for user in users:
        user.deactivate()


deactivate_users([User("foo"), Admin("bar_admin")])