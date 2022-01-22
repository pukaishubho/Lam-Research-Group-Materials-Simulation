# Created on Tue Jul 20 13:36:00 2021
'''
======================================================================
## neighbor list triplets
'''
import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
from scipy import stats
from glob import glob
import os
import csv

ds = []
angles = []
files2 = []
all_frames = []
b_length = 2.84
dmax = 2*b_length
buffer = 0.2

# n_atoms = 67
# n_bonds = 61

os.getcwd()
data_folder = os.path.join(os.getcwd(), 'frames_42_29_29')
len(list(os.walk(data_folder))[0][2])

for root, folders, files in os.walk(data_folder):
# for file in range(len(list(os.walk(data_folder))[0][2])):
	for file in files:
		zr_ids = []
		f_ids = []
		zrb_ids = []
		fb_ids = []
		zr_coord = []
		f_coord = []
		bonds = []
		match = []
		x_y_zs = []
		fx_y_zs = []
		zr1, zr2 = [], []
		pairs = []
		f_pairs = []
		path = os.path.join(root,file)
		xdatcar = open(path)
	# xdatcar = open(r"XDATCAR_42_full_FZr_bonds")
		data = xdatcar.readlines()

		n_atoms = int(data[1].split()[0])
		n_bonds = int(data[2].split()[0])
		na_start = 16
		nb_start = na_start+n_atoms+3
		xmax = float(data[5].split()[1])
		ymax = float(data[6].split()[1])
		zmax = float(data[7].split()[1])

		positions0 = data[na_start:na_start+n_atoms]
		# data = xdatcar.read()

		# for line in data:
		#     positions0 = line.split('Atoms  # bond')
		for element in positions0:
			xyz = element.split()
			a_id = float(xyz[0])
			c_id = float(xyz[2])
			if c_id == 2:
				zr_coord.append(xyz[0:6])
				zr_ids.append(xyz[0])
			else:
				f_ids.append(xyz[0])
				f_coord.append(xyz[0:6])
		# print(zr_coord)
		for j in range(len(zr_coord)):
			x_y_z = [int(zr_coord[j][0]), float(zr_coord[j][3]), float(zr_coord[j][4]), float(zr_coord[j][5])]
			x_y_zs.append(x_y_z)

		for j in range(len(f_coord)):
			fx_y_z = [int(f_coord[j][0]), float(f_coord[j][3]), float(f_coord[j][4]), float(f_coord[j][5])]
			fx_y_zs.append(fx_y_z)
   
		bonds0 = data[nb_start:nb_start+n_bonds]

		# for f_id in f_ids:
		for element in bonds0:
			bond = element.split()
			bonds.append(bond)
			fb_id = int(bond[2])
			zrb_id = int(bond[3])
			fb_ids.append(fb_id)
			zrb_ids.append(zrb_id)
			bond_ids = [fb_ids, zrb_ids]
    
		for f in range(1,len(bond_ids[0])):
			# print(f)
			f1 = bond_ids[0][f]
			f2 = bond_ids[0][f-1]
			if f1 == f2:
				chained = bond_ids[0][f], bond_ids[1][f], bond_ids[1][f-1]
				match.append(chained)
				# print(chained)

		for k in range(len(match)):
			# if re.search(chained[k][0], x_y_z):
			for kk in range(len(x_y_zs)):
				if match[k][1] == x_y_zs[kk][0]:
					# print(x_y_zs[kk][1:4])
					zr1 = x_y_zs[kk][1:4]
				if match[k][2] == x_y_zs[kk][0]:
					# print(x_y_zs[kk][1:4])
					zr2 = x_y_zs[kk][1:4]
				# coords = (zr1, zr2)
				coords = [zr1, zr2]
			pairs.append(coords)

		for k in range(len(match)):
			for kk in range(len(fx_y_zs)):
				if match[k][0] == fx_y_zs[kk][0]:
					f1 = fx_y_zs[kk][1:4]
				coordsf = [f1]
			f_pairs.append(coordsf)

		# print(pairs)

		## Wrap Zr at periodic boundaries
		for comb in range(len(pairs)):
			for c1 in range(len(pairs[comb])):
				for e1 in range(len(pairs[comb][c1])):
				#     # print(e1)
				#     # [pairs[comb][c1][e1]+xmax if pairs[comb][c1][e1] < 0 else pairs[comb][c1][e1] for pairs[comb][c1][e1] in pairs[comb][c1]]
				#     print(pairs)
					if (pairs[comb][c1][e1]) < 0:
						pairs[comb][c1][e1] = pairs[comb][c1][e1]+xmax
						# an = min(pairs[comb][c1])+xmax
						# print(min(pairs[comb][c1]))
					if (pairs[comb][c1][e1]) > xmax:
						pairs[comb][c1][e1] = pairs[comb][c1][e1]-xmax
		# print(pairs)                           

		## Wrap F at periodic boundaries
		for comb in range(len(f_pairs)):
			for c1 in range(len(f_pairs[comb])):
				for e1 in range(len(f_pairs[comb][c1])):
					if (f_pairs[comb][c1][e1]) < 0:
						f_pairs[comb][c1][e1] = f_pairs[comb][c1][e1]+xmax
						# an = min(pairs[comb][c1])+xmax
						# print(min(pairs[comb][c1]))
					if (f_pairs[comb][c1][e1]) > xmax:
						f_pairs[comb][c1][e1] = f_pairs[comb][c1][e1]-xmax

		for comb in range(len(pairs)):
			for c1 in range(len(pairs[comb])-1):
				d_int = np.sqrt((pairs[comb][c1][0]-pairs[comb][c1+1][0])**2+(pairs[comb][c1][1]-pairs[comb][c1+1][1])**2+(pairs[comb][c1][2]-pairs[comb][c1+1][2])**2)
				if d_int > dmax:
					for e1 in range(len(pairs[comb][c1])):
						d_int2 = pairs[comb][c1][e1]-pairs[comb][c1+1][e1]
						if d_int2 > dmax-buffer:
							pairs[comb][c1][e1] = pairs[comb][c1][e1]-xmax
						if d_int2 < -dmax+buffer:
							pairs[comb][c1][e1] = pairs[comb][c1][e1]+xmax
		# print(pairs)     

		for comb in range(len(f_pairs)):
			for c1 in range(len(pairs[comb])-1):
				fd_int = np.sqrt((f_pairs[comb][c1][0]-pairs[comb][c1][0])**2+(f_pairs[comb][c1][1]-pairs[comb][c1][1])**2+(f_pairs[comb][c1][2]-pairs[comb][c1][2])**2)
				if fd_int > dmax/2:
					for e1 in range(len(f_pairs[comb][c1])):
						fd_int2 = f_pairs[comb][c1][e1]-pairs[comb][c1][e1]
						if fd_int2 > (dmax-buffer)/2:
							f_pairs[comb][c1][e1] = f_pairs[comb][c1][e1]-xmax
						if fd_int2 < -(dmax+buffer)/2:
							f_pairs[comb][c1][e1] = f_pairs[comb][c1][e1]+xmax

		for p in range(len(pairs)):
			d_zr_zr=np.sqrt((pairs[p][0][0]-pairs[p][1][0])**2+(pairs[p][0][1]-pairs[p][1][1])**2+(pairs[p][0][2]-pairs[p][1][2])**2)
			# print(d_zr_zr)
			ds.append(d_zr_zr)
			# if d_zr_zr > 5.68:
				# print(d_zr_zr,file) 
			current_frame = float(file.split('.')[1])
			all_frames.append(current_frame)
			# print(current_frame)
			files2.append(file)
		#print(ds)
		#print(files2)

		for p in range(len(pairs)):
			zrf1=np.sqrt((f_pairs[p][0][0]-pairs[p][0][0])**2+(f_pairs[p][0][1]-pairs[p][0][1])**2+(f_pairs[p][0][2]-pairs[p][0][2])**2)
			zrf2=np.sqrt((f_pairs[p][0][0]-pairs[p][1][0])**2+(f_pairs[p][0][1]-pairs[p][1][1])**2+(f_pairs[p][0][2]-pairs[p][1][2])**2)
			num = (f_pairs[p][0][0]-pairs[p][0][0])*(f_pairs[p][0][0]-pairs[p][1][0])+(f_pairs[p][0][1]-pairs[p][0][1])*(f_pairs[p][0][1]-pairs[p][1][1])+(f_pairs[p][0][2]-pairs[p][0][2])*(f_pairs[p][0][2]-pairs[p][1][2])
			theta_zr_f_zr = np.arccos((num)/(zrf1*zrf2))*(180/np.pi)
			angles.append(theta_zr_f_zr)

print(type(ds),len(ds), min(ds), max(ds), len(all_frames), type(file))


data = np.column_stack([all_frames, ds, angles])
datafile_path = "path_to_save_file/d_theta.txt"
np.savetxt(datafile_path , data)

