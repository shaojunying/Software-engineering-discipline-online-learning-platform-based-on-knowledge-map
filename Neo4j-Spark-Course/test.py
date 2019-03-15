def helper(n):
    assert n >= 0
    if n == 0:
        print("前", 0, "项的阶乘是", 1)
        return 1
    result = n * helper(n - 1)
    print("前", n, "项的阶乘是", result)
    return result


n = 10
helper(n)
