"""
Python 3.14 兼容性补丁。

Python 3.14 移除了 super() 的 __dict__ 属性，
导致 Django 5.0 的 django.template.context.BaseContext.__copy__() 中
copy(super()) 调用失败。

此补丁修复 BaseContext.__copy__ 使其兼容 Python 3.14。
"""

import copy as _copy

from django.template import context as _context


def _patched_base_context_copy(self):
    """修复版 __copy__：Python 3.14 中 super() 无 __dict__，直接复制实例属性"""
    duplicate = self.__class__.__new__(self.__class__)
    duplicate.__dict__.update(self.__dict__)
    duplicate.dicts = self.dicts[:]
    return duplicate


_context.BaseContext.__copy__ = _patched_base_context_copy
