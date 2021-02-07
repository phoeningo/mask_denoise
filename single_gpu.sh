#echo $1 $2 $3 $4

input=$1
#echo $input
stack=${input/./_stack.star}
awk '{print $1}' $input >$stack
tmp=${input/.star/_child.star}


#awk '{ print }' $1 | awk '!x[$1]++' >$tmp
gpu=$2
tmpstack=${input/.star/_}

mpi=$3

export CUDA_VISIBLE_DEVICES=$[gpu-1]

Group_micrographs=`grep mrc $stack |wc |awk '{print int(($1)/'${mpi}')}'`

for j in $(seq 1 $mpi)
   do
#   echo $j
   m=$[(Group_micrographs+1) * (j-1)+1 ]
  
#   echo $m
   n=$[(Group_micrographs+1) * j]
 
#   echo $n

   sed -n "$m,$n p" $stack >${tmpstack}$m'_'$n.star

 #  cat ${tmpstack}$m'_'$n.star

  grep -f ${tmpstack}$m'_'$n.star $4> ${tmpstack}$j.star
 # cat ${tmpstack}'_'$j.star

   #sh single_gpu.sh tmpstack'_'$m'_'$n.star $j
   python ~/bin/patch_slices.py --part_star ${tmpstack}$j.star --mask J441/J441_oneside_mask.mrc --fade 0.2 --mrcs _oneside.mrcs  & 


   
   done
  


