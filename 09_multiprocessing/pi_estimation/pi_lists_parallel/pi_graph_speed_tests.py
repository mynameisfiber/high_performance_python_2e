"""Graph execution time for serial, threaded and processes forms of Pi estimation with lists"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
#  pi_lists_series, pi_lists_parallel 1 2 4 8, pi_lists_parallel --processes 1 2 4 8
speeds = np.array([[71.1],
                   [71.1, 71.0, 70.7, 71.0],
                   [71.0, 37.1, 18.1, 18.7]])

nbr_cores = np.array([[1],
                      [1, 2, 4, 8],
                      [1, 2, 4, 8]])

labels = np.array(["Serial", "Threads", "Processes"])

plt.figure(1)
plt.clf()
markers = ['-.o', '--x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2)
plt.annotate("Serial and Threads have similar execution time", (nbr_cores[0][0]+0.2, speeds[0][0]+0.9) )
plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(0, 80)
plt.xlim(0.5, 8.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title("Time to estimate Pi using objects with 100,000,000\ndart throws in series, threaded and with processes")
#plt.grid()
#plt.show()
plt.tight_layout()
plt.savefig("09_pi_lists_graph_speed_tests_threaded_processes.png")
