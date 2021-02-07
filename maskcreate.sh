input=$1
output=${input/.mrc/_mask.mrc}
`which relion_mask_create` --i $1 --o $output --lowpass 10 --ini_threshold $2 --extend_inimask $3 --width_soft_edge $4 --j 8 
