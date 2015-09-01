########################################################################################################################
# This is a job scheduler
#
# Author: david.maier@couchbase.com
#
# License: Apache2
#
########################################################################################################################

import sched, time, datetime


###################################################
# Run frequently by being rescheduled
#
###################################################
def run_freq(freq, scheduler, func, params):
    func(params)
    scheduler.enter(freq, 1, run_freq, (freq, scheduler, func, params))

###################################################
# Run first by being scheduled
#
###################################################
def run(YYYY, MM, DD, hh, mm, freq, func, params):
    scheduler = sched.scheduler(time.time, time.sleep)
    start_date = datetime.datetime(YYYY,MM,DD,hh,mm)
    scheduler.enterabs(time.mktime(start_date.timetuple()), 1, run_freq, (freq,scheduler,func, params))
    scheduler.run()