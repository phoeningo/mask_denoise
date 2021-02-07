input_star=$1

tmp_head=${input_star/data/head}
tmp_all=${input_star/data/all}
tmp_part=${input_star/data/part}
if [ -e tmp*star ] ; then 

  rm tmp*star
fi

head -n 50 $1 | grep -v mrc > $tmp_head
grep mrc $1 > $tmp_all
img=` awk '{if ($1=="_rlnImageName") print $2}' $tmp_head |sed 's/#//' `
echo img : $img

micro=` awk '{if ($1=="_rlnMicrographName") print $2}' $tmp_head |sed 's/#//' `
echo micro : $micro



x=` awk '{if ($1=="_rlnCoordinateX") print $2}' $tmp_head |sed 's/#//' `
echo psi : $x
y=` awk '{if ($1=="_rlnCoordinateY") print $2}' $tmp_head |sed 's/#//' `
echo rot : $y
z=` awk '{if ($1=="_rlnCoordinateZ") print $2}' $tmp_head |sed 's/#//' `
echo tilt : $z





dx=` awk '{if ($1=="_rlnOriginX") print $2}' $tmp_head |sed 's/#//' `
echo dx : $dx
dy=` awk '{if ($1=="_rlnOriginY") print $2}' $tmp_head |sed 's/#//' `
echo dy : $dy
dz=` awk '{if ($1=="_rlnOriginZ") print $2}' $tmp_head |sed 's/#//' `
echo dz : $dz



psi=` awk '{if ($1=="_rlnAnglePsi") print $2}' $tmp_head |sed 's/#//' `
echo psi : $psi
rot=` awk '{if ($1=="_rlnAngleRot") print $2}' $tmp_head |sed 's/#//' `
echo rot : $rot
tilt=` awk '{if ($1=="_rlnAngleTilt") print $2}' $tmp_head |sed 's/#//' `
echo tilt : $tilt




#cat $tmp_head > tmp_out.star

#awk '{print $'$angx'$'$angy',$'$rot',$'$tilt',$'$psi'}' $1
awk '{print $'$micro',$'$img',$'$x',$'$y',$'$z',$'$rot',$'$tilt',$'$psi',$'$dx',$'$dy',$'$dz'}' $tmp_all |sort -k 1 >$tmp_part
#awk '{print $'$img'}' $tmp_all >tmp_img.star
