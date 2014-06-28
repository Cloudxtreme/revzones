#! /usr/bin/env python

import argparse
import jinja2
import json
import netaddr
import os
from pprint import pprint
import sys
import string

def checkdata(data):
    # TODO
    return

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
                    rev = subnet[0].reverse_dns[2:]
                    s = { "net": subnet, "revzone": rev, "revzonend": rev[:-1] }
                    nets.append(s)
            if ip.version == 6:
                pl = ip.prefixlen
                while pl % 4 != 0:
                    pl = pl + 1
                for subnet in list(ip.subnet(pl)):
                    d = 32 - ( subnet.prefixlen / 4 )
                    rev = string.join(subnet[0].reverse_dns.split(".")[d:],".")
                    s = { "net": subnet, "revzone": rev, "revzonend": rev[:-1] }
                    nets.append(s)
    return nets

def render_bindmaster(env, data, subnet):
    tmpl = env.get_template("bindmaster.tmpl")
    net = subnet["net"]
    return tmpl.render(data=data, subnet=subnet)

def render_bindzone(env, data, subnet):
    tmpl = env.get_template("bindzone.tmpl")
    net = subnet["net"]
    return tmpl.render(data=data, subnet=subnet)

def render_ripedomain(env, data, subnet):
    tmpl = env.get_template("ripedomain.tmpl")
    net = subnet["net"]
    return tmpl.render(data=data, subnet=subnet)


def main():

    parser = argparse.ArgumentParser(description='Reverse zone geneator')
    parser.add_argument('-c', help='configuration filename',action='store',dest='cfgfile',required=True)
    args = parser.parse_args()

    if os.path.isfile(args.cfgfile) == False:
        print('Config file specified does not exist')
        sys.exit()

    json_data=open(args.cfgfile)
    data = json.load(json_data)
    json_data.close()

    checkdata(data)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"), trim_blocks=True)

    subnets = checksubnets(data["prefixes"])

#    render_bindmaster(data,subnets[0])

    if len(subnets) == 0:
        print "No subnets specified"
        sys.exit()

    for subnet in subnets:
       # print render_bindmaster(env, data, subnet)
       # print render_bindzone(env, data, subnet)
        print render_ripedomain(env, data, subnet)

    return


if __name__ == '__main__':
    main()
    exit(0)
