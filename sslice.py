import numpy as np
from pyrotate import *
from matrix import *
import pycuda.driver as cuda
from ftslice import *
from shift import *
from lib import method as M


def BW(arr):
  x,y=arr.shape
  for i in range(x):
    for j in range(y):
      if arr[i,j]>0.1:
        arr[i,j]=1
      else:
        arr[i,j]=0
  arr=None
  
def exec_time(current):
  print(time.time()-current)
  current=time.time()
  return current
  
def get_slice(input_volume,angle,dx,dy,seq='zyz'):
  output_volume=np.empty_like(input_volume)
  R=np.float32(euler2matrix(angle,seq))
  print('malloc device memory...')


  total_mem=cuda.mem_alloc(input_volume.nbytes+output_volume.nbytes+R.nbytes)

  a_gpu=total_mem
  b_gpu=int(a_gpu)+input_volume.nbytes 
  R_gpu=int(b_gpu)+output_volume.nbytes
  print('done.')

  cuda.memcpy_htod(a_gpu,input_volume)
  cuda.memcpy_htod(R_gpu,R)


  grid=input_volume.shape

  gpu_rotate(np.intp(a_gpu),np.intp(R_gpu),np.intp(b_gpu),grid)

  cuda.memcpy_dtoh(output_volume,b_gpu)
  volume_slice=zslice(output_volume)
  BW(volume_slice)
  print(dx,dy)
  volume_slice=shift(volume_slice,int(dx),int(dy))

  #print(volume_slice)
  return volume_slice


def thread_process(input_volume,dx,dy,output_list):
  #lock.acquire()
  tmp_slice=zslice(input_volume)

  tmp_slice=zslice(input_volume)
  BW(tmp_slice)
# not apply shift yet !!!
  tmp_slice=shift(tmp_slice,dx,dy)
  
  output_list.append(tmp_slice.copy())
  
  #output_list.append('x')
  #lock.release()
  #print('thread done')
  #_thread.exit()



def get_slices(input_volume,angles,shifts,a_gpu,b_init,R_init,output_volumes,seq='zyz'):
#  current=time.time()
  output_list=[]
  L=len(angles)
  #x,y,z=input_volume.shape
# ===BUG HERE !!!!!!!!!!!!!=== SHOULD USE INVMATRIX= 

# however change to this one .
  R=np.float32(euler2matrix(angles[0],seq))
#  print(R)
#  R=np.float32(invMatrix(angles[0],seq))
  #print('malloc device memory...')
#  output_volume=np.empty(shape=(x,y,z),dtype=np.float32)

  volume_size=input_volume.nbytes

  #a_gpu=cuda.mem_alloc(volume_size )
  #b_init=cuda.mem_alloc(volume_size*L)
  #R_init=cuda.mem_alloc(R.nbytes*L)

  #cuda.memcpy_htod(a_gpu,input_volume)
  grid=input_volume.shape

  count=0
  #stream=cuda.Stream()
  
  for angle in angles:
#    R=np.float32(euler2matrix(angle,seq))

    R=np.float32(invMatrix(angles[0],seq))
    R_gpu=int(R_init)+count*R.nbytes
    cuda.memcpy_htod(R_gpu,R)
    b_gpu=int(b_init)+count*volume_size
    #stream.synchronize()
    gpu_rotate(np.intp(a_gpu),np.intp(R_gpu),np.intp(b_gpu),grid)
    #stream.synchronize()
    count+=1
    #cuda.memcpy_dtoh(output_volume)
  cuda.memcpy_dtoh(output_volumes,b_init)
 # print('t1')

 # current=exec_time(current)
#  lock=_thread.allocate()

  for count in range(L):
 #   current=exec_time(current)
    tmp_v=output_volumes[count]
    dx,dy=shifts[count]
    thread_process(tmp_v,int(dx),int(dy),output_list)
    #_thread.start_new(thread_process,(tmp_v,int(dx),int(dy),output_list,lock))
    '''

    #volume_slice=zslice(output_volumes[count])
    print('t2')
    current=exec_time(current)

    #print(np.max(volume_slice))
    BW(volume_slice)
    print('t3')
    current=exec_time(current)

   # print(volume_slice)
   # M.write_pix_file(volume_slice,'test_mask.mrc',1)
    dx,dy=shifts[count]
    shift(volume_slice,int(dx),int(dy))
    print('t4')
    current=exec_time(current)

    output_list.append(volume_slice.copy())
    print('t5')
    current=exec_time(current)

    '''
  while(len(output_list)!=L):
    print(output_list)
  return output_list

