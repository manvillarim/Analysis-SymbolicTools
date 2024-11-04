def fibonacci(num):
    if num == 0:
        return 1
    else:
        return num * fibonacci(num - 1)


num = fibonacci(5)
print(num)
