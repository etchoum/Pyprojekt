# Pyprojekt
To calculate walltimes of computation node machines

# Aims
* parse `sacct` data to display the average waiting time over the last 7 days
  * classification data into bins based on partitions
  * bin data by requested timelimits
    * e.g. < 5min, 5-30m, 30m-2h, 2h-12h, 12-48, 48+
  * take number of requested cores into account
    * cores * timelimit = core-time as a metric to bin the data by
* Visualize this data on a web page, e.g. using flask

# Examples:

Example for `argp.py -p medium,fat`:
|partition| < 20CPUh |  20-600CPUh | >600CPUh| 
|---| ------ | ------ | ------ |
|medium| 10s | 5min |20min |
|fat| 1s | 20min | 2d |

Example for `argp.py -p medium,fat --mem`:
|partition| < 100GBh |  100GBh - 1Tbh | >1TBh| 
|---| ------ | ------ | ------ |
|medium| 10min | 2days |200days |
|fat| 1s | 20min | 2d |

Example for `argp.py --mem`:
|partition| < 100GBh |  100GBh - 1Tbh | >1TBh| 
|---| ------ | ------ | ------ |
|medium| 10min | 2days |200days |
|fat| 1s | 20min | 2d |
|fat+| 10min | 2days |200days |
|gpu| 1s | 20min | 2d |
|int| 1s | 20min | 2d |

Output should be divided in mor than three categories.

# Links

* [pep8 style guide](https://www.python.org/dev/peps/pep-0008/)
* [PyEcon](https://pyecon.org/lecture/)
