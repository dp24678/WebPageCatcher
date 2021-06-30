# -*- encoding: utf-8 -*-
import validators

url = 'https://-.-.-/en/latest/#'


status = validators.url(url)
# print(status)

def validators_url(url):
    status = validators.url(url)
    if status == True:
        return True
    else:
        return False


print(validators_url(url))