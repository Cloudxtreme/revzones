#! /usr/bin/env python

import argparse
import jinja2
import json
import netaddr
import os
import sys
import string
import time


def checkdata(data):
    # TODO
    return


def parsesubnets(src):
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
                    # split v6 on smallest bit boundry
                    rev = string.join(subnet[0].reverse_dns.split(".")[d:],".")
                    s = { "net": subnet, "revzone": rev, "revzonend": rev[:-1] }
                    nets.append(s)
    return nets


def val_yyyymmdd():
    return time.strftime("%Y%m%d")


def main():

    # load templates config
    templatesjson=open("templates/templates.json")
    tmpldata = json.load(templatesjson)
    templatesjson.close()

    tmplchoices = []
    for tmpl in tmpldata["templates"]:
        tmplchoices.append(tmpl["name"])

    # get user input
    parser = argparse.ArgumentParser(description='Reverse zone geneator')
    parser.add_argument('-c', help='configuration filename',action='store',dest='cfgfile',required=True)
    parser.add_argument('-t', help='template', action='store', dest='type', required=True, choices=tmplchoices)
    parser.add_argument('-o', help='output', action='store', dest='output', required=False, choices=['screen','file'], default='screen')
    args = parser.parse_args()

    # try to load config for prefixes
    if os.path.isfile(args.cfgfile) == False:
        print "Config file does not exist: %s" % (args.cfgfile)
        sys.exit()

    json_data=open(args.cfgfile)
    data = json.load(json_data)
    json_data.close()

    checkdata(data)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"), trim_blocks=True)
    env.globals.update(yyyymmdd=val_yyyymmdd)

    # make sure template exists
    tmplfile = "%s.tmpl" % (args.type)
    if os.path.isfile("templates/%s" % (tmplfile)) == False:
        print "Template file does not exist: %s" % (args.tmplfile)
        sys.exit()
    tmpl = env.get_template(tmplfile)

    # parse subnets, split on bit boundry etc
    subnets = parsesubnets(data["prefixes"])

    if len(subnets) == 0:
        print "No subnets specified"
        sys.exit()

    for subnet in subnets:
        content = tmpl.render(data=data, subnet=subnet)
        if args.output == "screen":
            print ""
            print content
            print ""

    return


if __name__ == '__main__':
    main()
    exit(0)
