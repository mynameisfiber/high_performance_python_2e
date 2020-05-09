import timeit


def fibonacci_list(num_items):
    numbers = []
    a, b = 0, 1
    while len(numbers) < num_items:
        numbers.append(a)
        a, b = b, a + b
    return numbers


def fibonacci_gen(num_items):
    a, b = 0, 1
    while num_items:
        yield a
        a, b = b, a + b
        num_items -= 1


def test_fibonacci(func, N):
    for i in func(N):
        pass


if __name__ == "__main__":
    setup = "from __main__ import " "(test_fibonacci, fibonacci_gen, fibonacci_list, N)"
    iterations = 1000

    for N in (2, 100, 1_000, 100_00):
        t = timeit.timeit(
            stmt=f"test_fibonacci(fibonacci_list, N)", setup=setup, number=iterations
        )
        print(
            f"fibonacci_list took {t / iterations:.5e}s to calculate {N} fibonacci numbers"
        )

        t = timeit.timeit(
            stmt=f"test_fibonacci(fibonacci_gen, N)", setup=setup, number=iterations
        )
        print(
            f"fibonacci_gen took {t / iterations:.5e}s to calculate {N} fibonacci numbers"
        )
