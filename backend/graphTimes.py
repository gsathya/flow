#! /usr/bin/python
# Ben Jones
# 6675 Advanced Internet Computing
# graphTimes.py: generate a cdf of run times and db sizes

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def create_cdf(title, filename, label, dataset):
    dataset.sort()
    datasetY = [float(y)/float(len(dataset)) for y in range(len(dataset))]
    plt.figure()
    plt.xlabel(label)
    plt.ylabel('Total Fraction of Routers')
    plt.title(title)
    plt.plot(dataset, datasetY)

    fontP = FontProperties()
    fontP.set_size('small')
#    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=2, prop=fontP)
#    plt.legend(loc= legendLoc, prop=fontP)
    # plt.xlim(-0.1, 1.1)
    # plt.ylim(-0.1, 1.1)
    plt.grid()

    plt.savefig(filename, format='png')

def get_data(filename):
    fileP = open(filename, 'r')
    data = []
    for line in fileP:
        data.append(int(line))
    return data

if __name__ == "__main__":
    sizes = get_data("6675-sizes.txt")
    times = get_data("6675-run-times.txt")
    times = [float(entry)/3600.0 for entry in times]
    sizes = [float(entry)/1024.0 for entry in sizes]
    create_cdf('CDf of Prevalence/Persistence Computation Times', 'times.png', 'Computational Time in Hours', times)
    create_cdf('CDf of Prevalence/Persistence DB Sizes', 'sizes.png', 'Size of Prevalence/Persistence DBs in KBs', sizes)
