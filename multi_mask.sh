if [ ! -d TMP ] ; then
mkdir TMP
fi
input=$1
tmp=${input/.part/_tmpstack.star}
awk '{ print }' $1 | awk '!x[$1]++' >$tmp
#echo $input
tmp_stack=${input/.part/_}
#echo $tmp_stack


#3*8
gpulist=0,1,2,3,4,5,6,7
gpus=$2
mpi=$3


Group_micrographs=`grep mrc $tmp |wc |awk '{print int(($1)/'${gpus}')}'`


for j in $(seq 1 $gpus)
   do
 #  echo $j
   m=$[(Group_micrographs+1) * (j-1)+1 ]
  
 #  echo $m
   n=$[(Group_micrographs+1) * j]
 
 #  echo $n

   sed -n "$m,$n p" $tmp > TMP/${tmp_stack}$m'_'$n.star
# echo sh single_gpu.sh TMP/${tmp_stack}$m'_'$n.star $j $mpi $input

   sh single_gpu.sh TMP/${tmp_stack}$m'_'$n.star $j $mpi $input 

   done
  
