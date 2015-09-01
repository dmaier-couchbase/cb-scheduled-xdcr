########################################################################################################################
# This is the 'cbschedulexdcr' command line tool
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

# Imports
import sys, xdcrclient, daemon, time, jobscheduler

###################################################
# Print the usage information
#
###################################################
def usage():
    print("Usage: python cbschedulexdcr.py {url} {user} {password} {source_bucket} {target_bucket} {target_cluster} {YYYY-MM-DD,hh:mm} {interval in seconds}")

###################################################
# Checks if the passed arguments are valid
#
# TODO: Implement
###################################################
def validate():
    print("Validating arguments ...")

    # The url format is http://{host}:{port}, whereby port is a number

    # The target cluster is not an url

    # The date format is {YYYY-MM-DD,hh:mm}

    # Interval is a number

    return True

###################################################
# Parse the date parameter which has the format
# YYYY-MM-DD,hh:mm
#
###################################################
def parse_data_arg(start_time):

    date_arr = start_time.split("-")
    year = date_arr[0]
    month = date_arr[1].lstrip("0")
    day_time = date_arr[2]
    day_time_arr = day_time.split(",")
    day = day_time_arr[0].lstrip("0")
    time = day_time_arr[1]
    time_arr = time.split(":")
    hour = time_arr[0].lstrip("0")
    minute = time_arr[1].lstrip("0")

    result = []
    result.append(int(year))
    result.append(int(month))
    result.append(int(day))
    result.append(int(hour))
    result.append(int(minute))

    return result

###################################################
# This function is executed by the job runner
#
# It runs the replication until all relevant data
# is replicated and then pauses again
#
###################################################
def run_and_pause(params):

    url = params["url"]
    user = params["user"]
    password = params["password"]
    source_bucket = params["source_bucket"]
    target_bucket = params["target_bucket"]
    target_cluster = params["target_cluster"]

    link_id = xdcrclient.link_id(url, user, password, source_bucket,target_bucket,target_cluster)
    complete = xdcrclient.ret_stat(url, user, password, source_bucket, link_id, "percent_completeness")

    print(complete)
    print("Starting replication ...")
    xdcrclient.pause(url,user,password,link_id,True)

    #TODO find out why the stat value stays sometimes at 100% even if data was added, maybe just an issue with the stat approx.
    # changes_left might be helpful, increased also if XDCR is paused

    while complete < 100.0:
        complete = xdcrclient.ret_stat(url, user, password, source_bucket, link_id, "percent_completeness")
        print("Comlete: " + str(complete))
        time.sleep(10)

    xdcrclient.pause(url, user, password, link_id)

    print("Replication finished.")

###################################################
# The entry point of the application
#
###################################################
def main(args = sys.argv):

    if len(args) == 9:
        print("Starting the daemon ...")

        #Run as daemon
        #daemon.daemonize("cb-scheduled-xdcr.pid")

        url = args[1]
        user = args[2]
        password = args[3]
        source_bucket = args[4]
        target_bucket = args[5]
        target_cluster = args[6]
        start_time = args[7]
        interval = float(args[8])

        #Parse the date
        start_time_arr = parse_data_arg(start_time)

        #Make sure that XDCR is paused
        link_id = xdcrclient.link_id(url, user, password, source_bucket,target_bucket,target_cluster)
        xdcrclient.pause(url,user,password,link_id)


        #Prepare the job  parameters and schedule the job
        params = { "url" : url, "user" : user, "password" : password, "source_bucket" : source_bucket,
                   "target_bucket" : target_bucket, "target_cluster" : target_cluster,
                   "start_time_arr" : start_time_arr, "interval" : interval }

        print("Scheduling the job ...")
        print("params = " + str(params))

        jobscheduler.run(start_time_arr[0],start_time_arr[1],start_time_arr[2],start_time_arr[3],start_time_arr[4],interval,run_and_pause,params)

    else:
        usage()



if __name__ == '__main__':
    main();
