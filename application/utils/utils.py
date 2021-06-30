# -*- coding: utf-8 -*-
"""辅助工具和装饰器"""
import validators
from flask import flash


def flash_errors(form, category="warning"):
    """闪现表单的所有错误."""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text} - {error}", category)


def validators_url(url: str):
    """
    传入待校验的url字符串
    :param url:
    :return:
    """
    if url is not str:
        return False

    status = validators.url(url)
    return True if status is True else False


if __name__ == '__main__':
    url = '2https://www.52pojie.cn/'
    print(validators_url(url=url))