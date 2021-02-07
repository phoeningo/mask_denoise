#print('importing lib')
#from matrix import *
from lib import method as M
import numpy as np
#from pyrotate import *
import argparse
from sslice import *
from shift import *
import sys
import math
import pycuda.autoinit
import pycuda.driver as cuda
#drv.init()
PI=math.pi
parser=argparse.ArgumentParser()
parser.add_argument('--part_star',type=str,default='sub160.star')
parser.add_argument('--img_star',type=str,default='tmp_img.star')
parser.add_argument('--output_str',type=str)
parser.add_argument('--mask',type=str,default='J229/mask.mrc')
parser.add_argument('--mrcs',type=str,default='_sub.mrcs')
parser.add_argument('--output_pool',type=int,default=24)
parser.add_argument('--fade',type=float,default=0.5)
args=parser.parse_args()


#cuda=drv.Device(0)

#print('reading  files')

lines=M.star_read(args.part_star)
stack_list=[]
mask=M.read_float_mrc(args.mask)

x,y,z=mask.shape
temp_R=np.float32(euler2matrix([0,0,0],'xyz'))
#init_output_pool_size=64
# 
max_output_size=args.output_pool
input_gpu=cuda.mem_alloc(mask.nbytes)
cuda.memcpy_htod(input_gpu,mask)
output_gpu=cuda.mem_alloc(mask.nbytes*max_output_size)
R_gpu=cuda.mem_alloc(temp_R.nbytes*max_output_size)
#
#global fade=args.fade

output_volumes=np.empty(shape=(max_output_size,x,y,z),dtype=np.float32)


def post():
  pass


def patch(stack_lines_sp,mask,a_gpu,b_gpu,R_gpu,out_stack,output_volumes):
  angles=[]
  shifts=[]
  Len=len(stack_lines_sp)
  for particle in stack_lines_sp:
    particle_sp=particle.split(' ')
    angle=[float(particle_sp[2])/180*PI,float(particle_sp[3])/180*PI,float(particle_sp[4])/180*PI]
    dx=float(particle_sp[5])
    dy=float(particle_sp[6])
    shifts.append([dx,dy])

    angles.append(angle)
  slices_mask=get_slices(mask,angles,shifts,a_gpu,b_gpu,R_gpu,output_volumes)  
  stack_name=stack_lines_sp[0].split(' ')[0]
  
  count=0
  for particle in stack_lines_sp: 
    particle_sp=particle.split(' ')
    index=int(particle_sp[1].split('@')[0])
    out_stack[index-1]=(args.fade+((1-args.fade)*slices_mask[count]))*img_stack[index-1]
    count+=1
   # print(stack_name+':'+str(count)+' / '+ str(Len)+', index :'+ str(index))
  assert count==Len

  


for line in lines:
  line_sp=line.split(' ')
  try:
    line_sp.remove('')
  except:
    pass
  try:
    stackname=line_sp[1].split('@')[1]
  except:
    #print(line_sp)
    continue
  if stackname not in stack_list:
    stack_list.append(stackname)

#print('done')
count=0
#print(stack_list)

for stack in stack_list:
  stack_lines=M.cmd_exec('grep '+stack+' '+args.part_star,1)
  #print(stack_lines)
  #sys.exit(1)
  stack_lines_sp=stack_lines.split('\n')
 # print(stack_lines)
  try:
    first_line=stack_lines_sp[0]
    img_stack_name=first_line.split(' ')[1]
    stack_name=img_stack_name.split('@')[1]
  except:
    continue
  try:
    stack_lines_sp.remove('')
  except:

    pass
  L=len(stack_lines_sp)


  print(stack_name+' : '+str(len(stack_lines_sp))+' particles')
  img_stack,angpix=M.read_pix_mrc(stack_name)
  out_stack=np.zeros(shape=img_stack.shape,dtype=img_stack.dtype)
  out_stack_name=stack_name.replace('.mrcs',args.mrcs)
  angles=[]
  shifts=[]
  if len(stack_lines_sp)<max_output_size:
   # print ('call Patch function , no need to devide for length '+str(L))
    patch(stack_lines_sp,mask,input_gpu,output_gpu,R_gpu,out_stack,output_volumes)
  else:
    patches=int(L/max_output_size)
    for pi in range(patches):
      each_patch_input=stack_lines_sp[pi*max_output_size:(pi+1)*max_output_size]
      patch(each_patch_input,mask,input_gpu,output_gpu,R_gpu,out_stack,output_volumes)
      
    #  print ('call Patch function ,for patch '+str(pi))
    reminder=stack_lines_sp[patches*max_output_size:]
    if reminder!=[]:
      patch(reminder,mask,input_gpu,output_gpu,R_gpu,out_stack,output_volumes)
  
    #print ('call Patch function ,for reminders' )
  M.write_pix_file(out_stack,out_stack_name,angpix)






