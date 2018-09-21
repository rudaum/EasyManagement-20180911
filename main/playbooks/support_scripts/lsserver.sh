lparstat -i | egrep "^Node Name |^Partition Number |^Type   |^Mode      |^Entitled Capacity   |^Online Memory   |^Online Virtu
al CPUs  " | awk -F":" '{sub(/[ ,]+$/,"",$1); print $1":"$2}' | sed 's/: /:/g'
echo "Oslevel:$(oslevel -s)"
lslpp -l cluster.es.server.rte >> /dev/null 2>&1
if [ $? -eq 0 ]; then
   clserv=$(/usr/es/sbin/cluster/utilities/cllsres | grep SERVICE_LABEL | cut -d'=' -f2)
   clnodes=$(/usr/es/sbin/cluster/utilities/cllsnode | grep -i "^Node " | awk '{print $2}'|sed 's/://g')
   echo Is Cluster:$clserv "($(echo $clnodes))"
else
   echo "Is Cluster:Not Clustered"
fi
ip=$(host $(hostname) | cut -d' ' -f3 | sed 's/,//g')
echo "IP Address:$ip"
