input_star=$1

tmp_head=${input_star/.star/.head}
tmp_all=${input_star/.star/.all}
tmp_part=${input_star/.star/.part}
# rm tmp*star
head -n 50 $1 | grep -v mrc > $tmp_head
grep mrc $1 > $tmp_all
img=` awk '{if ($1=="_rlnImageName") print $2}' $tmp_head |sed 's/#//' `
echo img : $img

micro=` awk '{if ($1=="_rlnMicrographName") print $2}' $tmp_head |sed 's/#//' `
echo micro : $micro



dx=` awk '{if ($1=="_rlnOriginX") print $2}' $tmp_head |sed 's/#//' `
echo dx : $dx
dy=` awk '{if ($1=="_rlnOriginY") print $2}' $tmp_head |sed 's/#//' `
echo dy : $dy

psi=` awk '{if ($1=="_rlnAnglePsi") print $2}' $tmp_head |sed 's/#//' `
echo psi : $psi
rot=` awk '{if ($1=="_rlnAngleRot") print $2}' $tmp_head |sed 's/#//' `
echo rot : $rot
tilt=` awk '{if ($1=="_rlnAngleTilt") print $2}' $tmp_head |sed 's/#//' `
echo tilt : $tilt




#cat $tmp_head > tmp_out.star

#awk '{print $'$angx'$'$angy',$'$rot',$'$tilt',$'$psi'}' $1
awk '{print $'$micro',$'$img',$'$rot',$'$tilt',$'$psi',$'$dx',$'$dy'}' $tmp_all |sort -k 1 >$tmp_part

#awk '{print $'$img'}' $tmp_all >tmp_img.star
