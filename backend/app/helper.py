import random


# 生成随机的字符串
def random_string(length=32):
    base_str = 'abcdefghijklnopqrstuvwxyz1234567890'
    return ''.join(random.choice(base_str) for i in range(length))
