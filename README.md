# Scheduled XDCR for Couchbase

Couchbase's Cross Data Center Replication is used in order to replicate the Bucket data from one Data Center to another one. XDCR can also be used bi-directionally by having built-in conflict solution. Use cases for XDCR are for instance:

* Data Locality
* Disaster Recovery
* Load Seperation

It's important to understand the difference between Disaster Recovery and Backup/Restore in the first step.

* Disaster Recovery means that you have another Data Center which has exaclty the same data and most often also a copy of the whole infrastructure. If the main Data Center fails then it is possible to switch over to the second Data Center. Couchbase supports this scenario directly via XDCR. Given the fact that you continiously replicate the data from the source cluster to the target cluster, XDCR does not provide any protection from data corruption, which means if you modify or delete data the wrong way on the source side then this will be propagated to the target side.

* Backup/Restore is different. In Couchbase the tools 'cbbackup'/'cbrestore' are existent. The tool cbbackup is used in order to make a copy of your bucket. This copy contains the actual state at the point of time when the backup was taken. So let's assume that you perform a differential backup every day, then you can recover the state of your bucket to yesterday's. This helps you to handle data corruption with the accurancy of the backup frequency.

The idea behind scheduled XDCR is to use XDCR by being able to hande data corruption with a specifc accurancy. So instead using a continous replication, we could replicate changes (mutations) over to the target bucket on a dayly basis and then additionally take the backup from there. This allows us to use the target cluster not as a Disaster Recovery Cluster, but as a Backup Cluster instead.

## Requirements

The following basic requirments are existent:

* The implementation should happen in one of Couchbase's native languages (Python, C/C++, Go, Erlang)
* Run a job/daemon which accepts the following parameters
  * Cluster: The url of the cluster's Admin service
  * User: Admin user
  * Password: Admin password
  * Start time: The date and time when the job starts the first time
  * Frequency: How often should XDCR run
* Transfer every change which is existent at the point of time when the job kicks in
* The source cluster is still online and so serves requests. So the job runs as a background task.

## Implementation idea

* Use the XDCR REST interface for pausing/resuming XDCR
* Monitor the XDCR queues in order to determine if the relevant data was already transfered
* Use the heuristic of a marker document. The marker document is created as soon as the jobs kicks in. The job checks frequently if the marker already arrived on the target side.

## Challenges

The last requirement could be challenge because XDCR is designed to work continously. Even if the DCP protocol should make sure that we keep up from the oldest to the latest mutation per partition (per vBucket, not globally - which is important here), there is the question how to make sure that we transfered all the relevant mutations whereby those could be a lot of mutations because XDCR may be paused for a while. 



  



