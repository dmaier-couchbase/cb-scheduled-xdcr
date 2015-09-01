########################################################################################################################
# This is the job scheduler test
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

import jobscheduler

###################################################
# The function which is executed by the job
#
###################################################
def hello(params):
    print(params["msg"])

###################################################
# Test if the job runs
#
# TODO: date and time needs to be overridden manually.
#
###################################################
def test_run():
    print("Testing to run a job ...")
    params = {"msg" : "Hello world"}
    jobscheduler.run(2015, 8, 31, 16, 19, 120, hello, params)

def main():
    test_run()

if __name__ == '__main__':
    main();
