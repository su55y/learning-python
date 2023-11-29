print(__import__('functools').reduce(lambda p,n: p+n if n%3==0 or n%5==0 else p,range(1000)))
