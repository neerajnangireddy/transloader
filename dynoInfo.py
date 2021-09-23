import psutil


def dynoStats():
    BOLD_START = "\033[1m"
    BOLD_END = "\033[0m"
    cpuPercent = "{} %".format(psutil.cpu_percent(1))
    memoryPercent = "{} %".format(psutil.virtual_memory().percent)
    diskPercent = "{} %".format(psutil.disk_usage("/").percent)
    # print(cpuPercent)
    # print(memoryPercent)
    # print(diskPercent)
    template = "{0}CPU :{1} {2}\n" \
               "{0}RAM :{1} {3}\n" \
               "{0}DISK :{1} {4}".format(BOLD_START, BOLD_END, cpuPercent,
                                         memoryPercent, diskPercent)
    return template


if __name__ == "__main__":
    dynoStats()

