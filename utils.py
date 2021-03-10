import matplotlib.pyplot as plt

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def safe_map(fun, list):
    mappedList = []
    for item in list:
        try:
            mappedList.append(fun(item))
        except Exception as e:
            # print(e)
            continue
    return mappedList

def hist_plot(data, bins, filename, xscale='linear'):
    plt.clf()
    plt.grid()
    plt.xscale(xscale)
    plt.hist(data, bins=bins, histtype='step')
    plt.savefig(f"out/{filename}.png")

def dump_dict(dict, filename):
    f = open(f"out/{filename}.txt", "w")
    for item in dict.items():
        f.write(f"{item[0]}: {item[1]}\n")
    f.close()