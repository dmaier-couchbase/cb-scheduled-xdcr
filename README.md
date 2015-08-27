# Scheduled XDCR for Couchbase

Couchbase's Cross Data Center Replication is used in order to replicate the Bucket data from one Data Center to another one. XDCR can also be used bi-directionally by having built-in conflict solution. Use cases for XDCR are for instance:

* Data Locality
* Disaster Recovery
* Load Seperation

It's important to understand the difference between Disaster Recovery and Backup/Restore in the first step.

* Disaster Recovery means that you have another Data Center which has exaclty the same data and most often also a copy of the whole infrastructure. If the main Data Center fails then it is possible to switch over to the second Data Center. Couchbase supports this scenario directly via XDCR. Given the fact that you continiously replicate the data from the source cluster to the target cluster, XDCR does not provide any protection from data corruption, which means if you modify or delete data the wrong way on the source side then this will be propagated to the target side.

* Backup/Restore is different. In Couchbase the tools 'cbbackup'/'cbrestore' are existent. The tool cbbackup is used in order to make a copy of your bucket. This copy contains the actual state at the point of time when the backup was taken. So let's assume that you perform a differential backup every day, then you can recover the state of your bucket to yesterday's. This helps you to handle data corruption with the accurancy of the backup frequency.

The idea behind scheduled XDCR is to use XDCR by being able to hande data corruption with a specifc accurancy. So instead using a continous replication, we could replicate changes (mutations) over to the target bucket on a dayly basis and then additionally take the backup from there. This allows us to use the target cluster not as a Disaster Recovery Cluster, but as a Backup Cluster instead.
