"""Graph execution time for serial, threaded and processes forms of Pi estimation with numpy"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
# pi_numpy_serial_blocks.py
# (serial.py - same as serial blocks but for 1 large array only)
# pi_numpy_parallel_worker.py
speeds = np.array([[2.46],
                   [2.46, 2.19, 2.13, 2.05],
                   [2.46, 1.61, 0.88, 0.85]])

nbr_cores = np.array([[1],
                      [1, 2, 4, 8],
                      [1, 2, 4, 8]])

labels = np.array(["Serial", "Threads", "Processes"])

plt.figure(1)
plt.clf()
markers = ['-.x', '--x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2)
plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(0, 3)
plt.xlim(0.5, 8.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title("Time to estimate Pi using numpy with 100,000,000\ndart throws in series, threaded and with processes")
#plt.grid()
#plt.show()
plt.tight_layout()
plt.savefig("09_pi_numpy_graph_speed_tests_threaded_processes.png")
