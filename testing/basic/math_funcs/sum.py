from functools import reduce

get_sum = lambda nums: reduce(lambda next, prev: next + prev, nums)
