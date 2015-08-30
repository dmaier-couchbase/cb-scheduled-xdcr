########################################################################################################################
# This is the 'cbschedulexdcr' command line tool
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

# Imports
import sys
import xdcrclient

def usage():
    print("Usage: python cbschedulexdcr.py {url} {user} {YYYY-MM-DD,hh:mm} {interval in minutes}")

def main(args = sys.argv):

    # parse command line options
    print(args)

    if len(args) == 5:
        print("Starting the daemon ...")

        #TODO

    else:
        usage()



if __name__ == '__main__':
    main();
