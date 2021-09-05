import requests
from bs4 import BeautifulSoup

HOST_URL = "http://www.alterink.com/"


def stats():
    content = requests.get(HOST_URL)
    soup = BeautifulSoup(content.text, "html.parser")
    server_stats = soup.find(id="server_stats")
    inuse = server_stats.find(id="inuse").text
    inuse_percent = server_stats.find(id="inusepercent").text
    total_inuse = ("{0}  ({1} %)".format(inuse, inuse_percent))
    free_space = server_stats.find(id="freespace").text
    disk_space = server_stats.find(id="diskspace").text
    cpu_load = server_stats.find(id="cpuload").text
    cpu_load = "{0} %".format(cpu_load)

    stats_template = "SERVER SPACE:\n" \
                     "In Use = {0}\n" \
                     "Free Space = {1}\n" \
                     "Disk Space = {2}\n\n" \
                     "CPU:\n" \
                     "cpu load = {3}\n\n".format(total_inuse, free_space,
                                                 disk_space, cpu_load)
    return stats_template


if __name__ == "__main__":
    stats()