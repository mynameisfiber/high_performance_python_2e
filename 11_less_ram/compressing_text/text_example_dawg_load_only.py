#pip instal DAWG failed
#https://github.com/pytries/DAWG/issues/31
#$ python text_example_dawg.py 
#pip install DAWG-Python
#installs ok, but it is a read-only version of a wrapper to DAWG
#https://pypi.org/project/DAWG-Python/

import time
import timeit
import text_example
import memory_profiler
import dawg # 

if __name__ == "__main__":
    print(("RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0])))
    t2 = time.time()
    words_dawg = dawg.DAWG()
    with open('words_dawg.saved', 'rb') as f:
        words_dawg.read(f)
    t3 = time.time()
    print(t3-t2)
    print(("RAM after load {:0.1f}MiB".format(memory_profiler.memory_usage()[0])))

    assert 'Zwiebel' in words_dawg
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in words_dawg",
                                  setup="from __main__ import words_dawg",
                                  number=1,
                                  repeat=10000))
    print(("Summed time to lookup word {:0.4f}s".format(time_cost)))
