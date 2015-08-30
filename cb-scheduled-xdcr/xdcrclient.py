########################################################################################################################
# This is the XDCR client
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

import urllib, urllib2, simplejson as json

#e.g. http://192.168.7.162:8091/pools/default/remoteClusters
XDCR_REMOTE_CLUSTERS_ENDPOINT = "{url}/pools/default/remoteClusters"

#e.g. http://192.168.7.162:8091/pools/default/buckets/social/stats/replications%2F8106b17d57837763c1906bf1dd4d01cb%2Fsocial%2Ftest_xdcr%2Fpercent_completeness?haveTStamp=1440769218401&resampleForUI=1&zoom=minute&_=1440769218384
# {xdcr_stat}: e.g. percent_completeness
XDCR_STATS_ENDPOINT = "{url}/pools/default/buckets/{bucket}/stats/replications%2F{xdcr_link_id}%2F{xdcr_stat}"

#e.g. http://192.168.7.162:8091/settings/replications%2F8106b17d57837763c1906bf1dd4d01cb%2Fsocial%2Ftest_xdcr
XDCR_PAUSE_ENDPOINT = "{url}/settions/replications/{xdcr_link_id}"


###################################################
# Performs a GET by returning the result as JSON
#
###################################################
def rest_get(url, user, password):

    pwd_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pwd_mgr.add_password(None, url, user, password)
    handler =  urllib2.HTTPBasicAuthHandler(pwd_mgr)
    opener = urllib2.build_opener(handler)
    response = opener.open(url)
    result = json.load(response)

    return result


###################################################
# Returns the uuid of a cluster reference name
#
###################################################
def resolve_uuid(base_url, user, password, name):

    url = XDCR_REMOTE_CLUSTERS_ENDPOINT.replace("{url}", base_url)
    json_arr = rest_get(url, user, password)

    for entry in json_arr:
        if entry["name"] == name:
            return entry["uuid"]


###################################################
# Returns fully qualified cluster reference
#
# The XDCR link is identified by
# {ref_uuid}%2F{source_bucker}%2F{target_bucket} .
#
###################################################
def link_id(base_url, user, password, s_bucket, t_bucket, name):

    uuid = resolve_uuid(base_url,user,password,name)
    return uuid + "%2F" + s_bucket + "%2F" + t_bucket


###################################################
# Retrieves an XDCR statistics value
#
###################################################
def ret_stat(base_url, user, password, s_bucket, xdcr_link, stat):

    url = XDCR_STATS_ENDPOINT.replace("{url}", base_url)
    url = url.replace("{bucket}", s_bucket)
    url = url.replace("{xdcr_link_id}", xdcr_link)
    url = url.replace("{xdcr_stat}", stat)

    #TODO Parse the result
    return rest_get(url, user, password)


#TODO: Implement the pause/continue functionality