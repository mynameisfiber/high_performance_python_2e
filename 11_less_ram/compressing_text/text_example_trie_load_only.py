import time
import timeit
import text_example
import memory_profiler
import marisa_trie

if __name__ == "__main__":

    print("RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    print("RAM before loading from disk {:0.1f}MiB".format(memory_profiler.memory_usage()[0]))
    t2 = time.time()
    d = marisa_trie.Trie()
    with open('words_trie.saved', 'rb') as f:
        words_trie = d.read(f)
    t3 = time.time()
    print("RAM after loading trie from disk {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t3 - t2))
    print("The trie contains {} words".format(len(words_trie)))
    print(f"time to load {t3-t2:f}s")
    assert 'Zwiebel' in words_trie
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in words_trie",
                                  setup="from __main__ import words_trie",
                                  number=1,
                                  repeat=10000))
    print("Summed time to lookup word {:0.4f}s".format(time_cost))
    
