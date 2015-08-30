########################################################################################################################
# This is the test script for the XDCR Client
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

# Imports
import sys
import xdcrclient

BASE_URL = "http://192.168.7.162:8091"
ADMIN_USER = "couchbase"
ADMIN_PWD = "couchbase"

###################################################
# Test if the REST service is reachable
#
###################################################
def test_rest_get():

    print("Testing to get data from the service ...")
    result = xdcrclient.rest_get(BASE_URL + "/pools/default", ADMIN_USER, ADMIN_PWD)
    print(result)
    assert "rebalanceProgressUri" in str(result)

###################################################
# Test if the resolution from a name to the
# XDCR link's UUID works
#
# An XDCR link called 'local' is required for this
# purpose
###################################################
def test_resolve_uuid():
    print("Testing to resolve the UUID of the XDCR replicaton ...")
    result = xdcrclient.resolve_uuid(BASE_URL, ADMIN_USER, ADMIN_PWD, "local")
    print(result)
    assert len(result) == 32

###################################################
# Test if the access if the stats service works
#
# An XDCR link called 'local' with a source bucket
# 'social' and a target bucket 'test_xdcr' is required
###################################################
def test_ret_stat():
    print("Testing to retrive statistics ...")

    link_id = xdcrclient.link_id(BASE_URL, ADMIN_USER, ADMIN_PWD,"social","test_xdcr","local")
    print(link_id)

    result = xdcrclient.ret_stat(BASE_URL, ADMIN_USER, ADMIN_PWD, "social", link_id, "percent_completeness")
    print result
    #TODO Add assertion


def main():
       test_rest_get()
       test_resolve_uuid()
       test_ret_stat()

if __name__ == '__main__':
    main();
