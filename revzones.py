#! /usr/bin/env python

import netaddr
import jinja2

def checksubnets(src):
    nets = []
    for addr in src:
        ip = None
        try:
            ip = netaddr.IPNetwork(addr)
        except:
            ip = None
        if ip != None:
            if ip.version == 4:
                for subnet in list(ip.subnet(24)):
                    nets.append(subnet)
            if ip.version == 6:
                pl = ip.prefixlen
                while pl % 4 != 0:
                    pl = pl + 1
                for subnet in list(ip.subnet(pl)):
                    nets.append(subnet)
    return nets


def main():

    src = []
    src.append("195.177.252.0/23")
    src.append("193.47.147.0/24")
    src.append("2a04:ec40::/29")
    src.append("2001:67c:1b40::/46")
    src.append("2001:8b0:1200::/48")

    subnets = checksubnets(src)

    for subnet in subnets:
        print ""
        print subnet
      #  print subnet[0].reverse_dns

    return


if __name__ == '__main__':
    main()
    exit(0)