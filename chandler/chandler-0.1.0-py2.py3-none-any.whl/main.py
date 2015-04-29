#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from natsort import natsorted
import sys
import time
import re
from optparse import OptionParser
from collections import defaultdict
from colorama import Fore, Back, Style

from .configuration import Configuration
from .utils import (get, cprint, init_colorama, reraise,
                    unset_proxy_from_env)


def run(options, args):
    config = Configuration()
    init_colorama()

    # Get rid of http_proxy if necessary
    if config.ignore_proxy:
        unset_proxy_from_env()

    # Print a waiting message
    print('Querying OAR API...\n\033[1A'),

    # Get the data from the API
    # TODO: paginated results management
    resources = get('/resources/details', config,
                    reload_cache=options.reload_cache)['items']
    jobs = get('/jobs/details', config,
               reload_cache=options.reload_cache)['items']

    # Erase the waiting message
    print("\033[2K")

    # Compute assigned resources dictionnary
    assigned_resources = {r["id"]: j["types"] for j in jobs
                          for r in j["resources"]
                          if r["status"] == "assigned"}

    # Compute sorted node list
    nodes = natsorted(set([r["network_address"] for r in resources]))

    # Get the comment property if necessary
    if config.comment_property:
        comment = {r["network_address"]: r[config.comment_property]
                   for r in resources}

    # Loop on nodes and resources
    col = 0
    down = 0
    for node in nodes:
        c = 0
        node_resources = [r for r in resources if r["network_address"] == node]
        p = re.match(config.nodename_regex, node)
        node_str = p.group(1)
        if config.comment_property:
            node_str += " (" + comment[node] + ")"
        else:
            node_str += ": "
        string = node_str + " " * (config.col_span - len(node_str))
        cprint(Fore.RESET + Back.RESET + string)
        for r in node_resources:
            c += 1
            if r["state"] == "Dead":
                down += 1
                cprint(Back.RED + Fore.WHITE + "D")
            elif r["state"] == "Absent":
                if int(r["available_upto"]) > time.time():
                    cprint(Back.CYAN + Fore.WHITE + " ")
                else:
                    down += 1
                    cprint(Back.RED + Fore.WHITE + "A")
            elif r["state"] == "Suspected":
                down += 1
                cprint(Back.RED + Fore.WHITE + "S")
            elif r["state"] == "Alive":
                try:
                    types = assigned_resources[r["id"]]
                except:
                    cprint(Back.GREEN + Fore.WHITE + " ")
                else:
                    if "besteffort" in types:
                        cprint(Back.GREEN + Fore.BLACK + "B")
                    elif "timesharing" in types:
                        cprint(Back.YELLOW + Fore.BLACK + "T")
                    else:
                        cprint(Back.WHITE + Fore.BLACK + "J")
        cprint(Fore.RESET + Back.RESET)
        col += 1
        if col < config.cols and node not in config.separations:
            cprint(" " * (config.col_size - config.col_span - c))
        else:
            col = 0
            print

    # Legend
    print(Fore.RESET + Back.RESET)
    print
    cprint(Back.GREEN + " " + Back.RESET + "=Free ")
    cprint(Back.GREEN + Fore.BLACK + "B" +
           Back.RESET + Fore.RESET + "=Besteffort ")
    cprint(Back.CYAN + " " + Back.RESET + "=Standby ")
    cprint(Back.WHITE + Fore.BLACK + "J" + Back.RESET + Fore.RESET + "=Job ")
    cprint(Back.RED + Fore.BLACK + "S" +
           Back.RESET + Fore.RESET + "=Suspected ")
    cprint(Back.RED + Fore.BLACK + "A" + Back.RESET + Fore.RESET + "=Absent ")
    cprint(Back.RED + Fore.BLACK + "D" + Back.RESET + Fore.RESET + "=Dead ")
    print

    # Reset terminal styles
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    # Print summary
    print "{} jobs, {} resources, {} down, {} used".format(len(jobs),
                                                           len(resources),
                                                           down,
                                                           len(assigned_resources))

    # Print users stats if necessary
    if config.users_stats_by_default ^ options.toggle_users and len(jobs) > 0:
        print
        user_resources = defaultdict(int)
        user_running = defaultdict(int)
        user_waiting = defaultdict(int)
        user_nodes = defaultdict(list)
        for j in jobs:
            if (j["state"] == "Running" or j["state"] == "Finishing"
                    or j["state"] == "Launching"):
                user_running[j["owner"]] += 1
                user_resources[j["owner"]] += len(j["resources"])
                user_nodes[j["owner"]] += [n["network_address"]
                                           for n in j["nodes"]]
            elif j["state"] == "Waiting":
                user_waiting[j["owner"]] += 1
                user_resources[j["owner"]] += 0
                user_nodes[j["owner"]] += []

        print "               Jobs       Jobs"
        print "User          running    waiting   Resources    Nodes"
        print "====================================================="
        for u, r in user_resources.iteritems():
            nodes = set(user_nodes[u])
            print "{:<16} {:<10} {:<10} {:<10} {:<10}".format(u, user_running[u],
                                                              user_waiting[u],
                                                              r, len(nodes))

    # Print nodes usage if necessary
    if config.nodes_usage_by_default ^ options.toggle_nodes and len(jobs) > 0:
        print
        assigned_nodes = [[r["network_address"], j]
                          for j in jobs
                          for r in j["nodes"] if r["status"] == "assigned"]
        nodes_usage = defaultdict(list)
        for c in assigned_nodes:
            nodes_usage[c[0]].append(c[1])
        print config.nodes_header
        for node in natsorted(nodes_usage.keys()):
            print node + ":"
            for job in nodes_usage[node]:
                remain_time = job["start_time"] + job["walltime"] - time.time()
                d = time.strftime("%H:%M:%S", time.gmtime(remain_time))
                r = [r for r in resources if r["network_address"] ==
                     node and r["id"] in [rj["id"] for rj in job["resources"]]]
                print("    " + config.nodes_format.format(job["id"], job["owner"],
                                                          str(job["name"]), len(r),
                                                          ",".join(job["types"]),
                                                          d, job["project"]))


def main():
    # Options parsing
    parser = OptionParser()
    parser.add_option("-u", "--users",
                      action="store_true", dest="toggle_users", default=False,
                      help="Toggle printing users stats")
    parser.add_option("-n", "--nodes",
                      action="store_true", dest="toggle_nodes", default=False,
                      help="Toggle printing nodes usage")
    parser.add_option("-r", "--reload-cache",
                      action="store_true", dest="reload_cache", default=False,
                      help="Reload the cache")
    parser.add_option("--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enable debug mode")
    (options, args) = parser.parse_args()

    try:
        run(options, args)
    except:
        exc_type, exc_value, tb = sys.exc_info()
        if not options.debug:
            sys.stderr.write("%s\n" % exc_value)
            sys.exit(1)
        else:
            reraise(exc_type, exc_value, tb.tb_next)
