#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_____, ___
   '+ .;
    , ;
     .

       .
     .;.
     .;
      :
      ,


┌─[Vailyn]─[~]
└──╼ VainlyStrain
"""


import sys
import argparse
from core.colors import color


class ArgumentParser(argparse.ArgumentParser):
    """
    Vailyn's argument parser
    """
    def error(self, message):
        self.print_help()
        self.exit(2, "\n" + color.R + '[-]' + color.END + color.BOLD + ' Invalid/missing params'
                  + color.END + '\n' + color.RD + '[HINT]' + color.END + ' %s\n' % (message))

    def print_help(self):
        self.print_usage(sys.stderr)
        print('''
mandatory:
  -v VIC, --victim VIC  {0}Target to attack, part 1 [pre-payload]{1}
  -a INT, --attack INT  {0}Attack type (int, 1-5){1}

  {2}  1{1}{3}|;{1}  Query Parameter {2}  4{1}{3}|:{1}  POST Data
  {2}  2{1}{3}|:{1}  Path            {2}  5{1}{3}|;{1}  Crawler (automatic)
  {2}  3{1}{3}|;{1}  Cookie

  -l FIL PATH, --lists FIL PATH
                        {0}Dictionaries (files and dirs){1}
additional:
  -p P, --param P       {0}query parameter to use for --attack 1{1}
  -s D, --post D        {0}POST Data (set injection point with INJECT){1}
  -j A P, --listen A P  {0}Try a reverse shell in Phase 2 (A:IP, P:port){1}
  -d I J K, --depths I J K
                        {0}depths (I: phase 1, J: phase 2, K: permutation level){1}
  -n, --loot            {0}Download found files into the loot folder{1}
  -c C, --cookie C      {0}File containing authentication cookie (if needed){1}
  -h, --help            {0}show this help menu and exit{1}
  -i F, --check F       {0}File to check for in Phase 1 (df: /etc/passwd){1}
  -q V, --vic2 V        {0}Attack Target, part 2 [post-payload]{1}
  -t, --tor             {0}Pipe attacks through the Tor anonymity network{1}
  -k T, --timeout T     {0}Request Timeout; stable switch for Arjun{1}
  -m, --nosploit        {0}skip Phase 2 (does not need -l FIL PATH){1}
  --app                 {0}Start Vailyn's Qt5 interface{1}

develop:
  --debug               {0}Display every path tried, even 404s.{1}
  --version             {0}Print program version and exit.{1}'''.format(color.RC, color.END, color.BOLD, color.RD))


class VainFormatter(argparse.RawDescriptionHelpFormatter):
    """
    Formatter for the argument parser
    """
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = color.RC + 'Vsynta ' + color.END
            return super(VainFormatter, self).add_usage("{}Vailyn{} -v VIC -a INT -l FIL PATH \n".format(color.RB, color.END)
                                                        + "        [-p P] [-s D] [-j A P] [-n] \n      [-c C] [-i F] [-t] "
                                                        + "[-m] \n       [-k T] [-d I J K] \n"
                                                        + "   [-q V] [--app] ", actions, groups, prefix)


def build_parser():
    """
    constructs and returns an argument parser
    """
    p = ArgumentParser(formatter_class=VainFormatter, add_help=False)
    p.add_argument('-v', '--victim',
                   help="Target to attack, part 1 [pre injection point]",
                   metavar="VIC")
    p.add_argument('-a', '--attack',
                   help="Attack type (int, 1-4)[see the Markdown docs]",
                   metavar="INT",
                   type=int)
    p.add_argument('-k', '--timeout',
                   help="Request Timeout; stable switch for Arjun",
                   metavar="T",
                   type=int)
    p.add_argument('-s', '--post',
                   help="POST Data (set injection point with INJECT)",
                   metavar="D",)
    p.add_argument('-d', '--depths',
                   help="depths (I: phase 1, J: phase 2, K: permutation level)",
                   metavar="I J K",
                   type=int,
                   nargs=3)
    p.add_argument('-h', '--help',
                   help="0 » display this help message and exit",
                   action="help",
                   default=argparse.SUPPRESS)
    p.add_argument('-p', '--param',
                   help="query parameter to use for --attack 1",
                   metavar="P")
    p.add_argument('-l', '--lists',
                   help="Dictionaries to use (see templates for syntax)",
                   nargs=2,
                   metavar=("FIL", "PATH"))
    p.add_argument('-j', '--listen',
                   help="IP and port listening for shells (-a 5)",
                   nargs=2,
                   metavar=("A", "P"))
    p.add_argument('-n', '--loot',
                   help="Download found files into the loot folder",
                   action="store_true")
    p.add_argument('-q', '--vic2',
                   help="Attack Target, part 2 (post injection point)",
                   metavar=("V"))
    p.add_argument('-i', '--check',
                   help="File to check for in Phase 1 (df: /etc/passwd)",
                   metavar=("F"))
    p.add_argument('-c', '--cookie',
                   help="File containing authentication cookie (if needed)",
                   metavar=("C"))
    p.add_argument('-t', '--tor',
                   help="Pipe attacks through the Tor anonymity network",
                   action="store_true",)
    p.add_argument('--debug',
                   help="display every path tried, even 404s",
                   action="store_true",)
    p.add_argument('-m', '--nosploit',
                   help="skip Phase 2 (does not need -l FIL PATH)",
                   action="store_true",)
    p.add_argument('-g', '--app',
                   help="Start Vailyn's Qt5 interface",
                   action="store_true",)
    p.add_argument('--version',
                   help="Print program version and exit.",
                   action="store_true",)

    return p
