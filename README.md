High Performance Python 2e: The Code
=================================

This repository contains the code from ["High Performance
Python 2e"](http://shop.oreilly.com/product/0636920268505.do) by Micha Gorelick
and Ian Ozsvald with O'Reilly Media.  Each directory contains the examples from
the chapter in addition to other interesting code on the subject.

You can find out more about the authors here:

* https://github.com/mynameisfiber
* http://micha.codes/
* https://github.com/ianozsvald/
* https://ianozsvald.com/
  * Ian's twice-a-month newsletter contains Higher Performance and Data Science tips: https://ianozsvald.com/data-science-jobs/
  * Ian runs a training course on Higher Performance - see https://ianozsvald.com/training/
* https://twitter.com/ianozsvald

Errata
------

Errata can be filed here https://www.oreilly.com/cs/catalog/create/errata/?b=68228 (no login required, just a form with a few details) or you can check the confirmed errata here: https://www.oreilly.com/catalog/errata.csp?isbn=0636920268505 or file a bug on this repo, whatever's easiest.


Topics Covered
--------------

This book ranges in topic from native Python to external modules to writing your
own modules.  Code is shown to run on one CPU, multiple coroutines, multiple
CPU's and multiple computers.  In addition, throughout this exploration a focus
is kept on keeping development time fast and learning from profiling output in
order to direct optimizations.

The following topics are covered in the code repo:


- Chapter 1: Understanding Performant Programming
    * How can I identify speed and RAM bottlenecks in my code?
    * How do I profile CPU and memory usage?
    * What depth of profiling should I use?
    * How can I profile a long-running application?
    * What's happening under the hood with CPython?
    * How do I keep my code correct while tuning performance?

- Chapter 2: Profiling
    * What are the elements of a computer's architecture?
    * What are some common alternate computer architectures?
    * How does Python abstract the underlying computer architecture?
    * What are some of the hurdles to making performant Python code?
    * What strategies can help you become a highly performant programmer?

- Chapter 3: Lists and Tuples
    * What are lists and tuples good for?
    * What is the complexity of a lookup in a list/tuple?
    * How is that complexity achieved?
    * What are the differences between lists and tuples?
    * How does appending to a list work?
    * When should I use lists and tuples?

- Chapter 4: Dictionaries and Sets
    * What are dictionaries and sets good for?
    * How are dictionaries and sets the same?
    * What is the overhead when using a dictionary?
    * How can I optimize the performance of a dictionary?
    * How does Python use dictionaries to keep track of namespaces?

- Chapter 5: Iterators
    * How do generators save memory?
    * When is the best time to use a generator?
    * How can I use +itertools+ to create complex generator workflows?
    * When is lazy evaluation beneficial, and when is it not?

- Chapter 6: Matrix and Vector Computation
    * What are the bottlenecks in vector calculations?
    * What tools can I use to see how efficiently the CPU is doing my calculations?
    * Why is `numpy` better at numerical calculations than pure Python?
    * What are ++cache-miss++es and ++page-fault++s?
    * How can I track the memory allocations in my code?
    * How does Pandas work and how can I make it faster?

- Chapter 7: Compiling to C
    * How can I have my Python code run at compiled speeds?
    * What is the difference between a JIT compiler and an AOT compiler?
    * What tasks can compiled Python code perform faster than native Python?
    * Why do type annotations speed up compiled Python code?
    * What is a GPU and how can I use it?
    * When are GPUs useful?
    * How can I write modules for Python using C or Fortran?

- Chapter 8: Concurrency
    * What is concurrency and how is it helpful?
    * What is the difference between concurrency and parallelism?
    * How does async/await work?
    * Which tasks can be done concurrently and which can't?
    * When is the right time to take advantage of concurrency?
    * How can concurrency speed up my programs?

- Chapter 9: Multiprocessing
    * What does the ++multiprocessing++ module offer?
    * What's the difference between processes and threads?
    * How do I choose the right size for a process pool?
    * How do I use nonpersistent queues for work processing?
    * What are the costs and benefits of interprocess communication?
    * How can I process ++numpy++ data with many CPUs?
    * How would I use Joblib to simplify parallelised and cached scientific work?
    * Why do I need locking to avoid data loss?

- Chapter 10: Clusters and Job Queues
    * Why are clusters useful? 
    * What are the costs of clustering?
    * How can I convert a multiprocessing solution into a clustered solution?
    * How does an IPython cluster work?
    * How can I parallelise Pandas using Dask and Swifter?
    * How does NSQ help with making robust production systems?
    * What is Docker and how can I use it in my workflow?

- Chapter 11: Using Less Ram
    * Why should I use less RAM?
    * Why are `numpy` and `array` better for storing lots of numbers?
    * How can lots of text be efficiently stored in RAM?
    * How can I store huge volumes of text for machine learning when I don't have enough RAM?
    * When can sparse arrays beat normal dense arrays? 
    * How could I count (approximately!) to 10<sup>76</sup> using just 1 byte?
    * What is the landscape of Bloom Filters, HLL’s and KMVs?
    * When should I use a probabilistic datastructure?

- Chapter 12: Lessons from the Field (no code)
    * Some stories from the field on performance python


Using the code base
-------------------

This code base is a live document and should be freely commented on and used.
It is distributed with a license that amounts to: don't use the code for
profit, however read the [provided license](LICENSE.md) file for the
law-jargon.  Feel free to share, fork and comment on the code!

If any errors are found, or you have a bone to pick with how we go about doing
things, leave an issue on this repo!  Just keep in mind that all code was
written for educational purposes and sometimes this means favouring readability
over "the right thing" (although in Python these two things are generally one
and the same!).

