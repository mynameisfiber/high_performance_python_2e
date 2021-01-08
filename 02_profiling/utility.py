import time

def test_some_fn():
    """Check basic behaviours for our function"""
    assert some_fn(2) == 4
    assert some_fn(1) == 1
    assert some_fn(-1) == 1


# check for line_profiler or memory_profiler in the local scope, both
# are injected by their respective tools or they're absent
# if these tools aren't being used (in which case we need to substite
# a dummy @profile decorator)
if 'line_profiler' not in dir() and 'profile' not in dir():
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner

@profile
def some_fn(useful_input):
    """An expensive function that we wish to both test and profile"""
    # artificial 'we're doing something clever and expensive' delay
    time.sleep(1) 
    return useful_input ** 2


if __name__ == "__main__":
    print(f"Example call `some_fn(2)` == {some_fn(2)}")


