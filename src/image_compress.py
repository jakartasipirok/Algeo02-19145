from PIL import Image
import numpy as np
import math
import time
from svd import*

def compress_svd(img_mat,k):
	#BAGIAN YANG DIKOMENTARI DIGANTI DENGAN ALGORITMA BUATAN SENDIRI
	#Untuk testing, silahkan uncomment baris kode di bawah ini.
	U,Sigma,Vt = svdmethod(img_mat)
	reconst_mat = np.dot(U[:,:k], np.dot(np.diag(Sigma[:k]), Vt[:k,:]))
	return reconst_mat

def percentage_convert(image, percentage):
	return (percentage * (image.size[0]*image.size[1])) / (100 * (image.size[0] + image.size[1]))

def img_compress(filename,percentage):
	"""
	FUNGSI UTAMA UNTUK ME-COMPRESS GAMBAR
	Input filename : berisi file gambar (contoh.jpg). Untuk pengaturan path nya belum dikerjakan sehingga gambar harus ditaruh di
	directory yang sama dengan file ini.
	Input percentage : compression level
	belum rapi sih.

	RETURNS TIME
	"""
	#start timer
	start = time.time()
	#Membuka file dan dijadikan bentuk matriks
	img = Image.open('static/uploads/'+filename)
	img_mat = np.asarray(img).astype(float)
	#convert presentase input menjadi k
	k = int(math.ceil(percentage_convert(img, percentage)))

	#setiap channel warna dipisahkan (rgb). Pada img_mat, matriksnya adalah 3 dimensi dan pada dimensi ketiganya, indeks 0-2 adalah r,g,b
	mat_r = img_mat[:,:,0]
	mat_g = img_mat[:,:,1]
	mat_b = img_mat[:,:,2]

	#Dicompress dengan nilai k pada masing-masing channel warna.
	mat_compressed = []
	mat_compressed.append(compress_svd(mat_r,k))
	mat_compressed.append(compress_svd(mat_g,k))
	mat_compressed.append(compress_svd(mat_b,k))

	#Semua matriks warna yang udah dikompress dijadikan satu lagi.
	img_reconstruct = np.zeros(img_mat.shape)
	for i in range(3):
		img_reconstruct[:,:,i] = mat_compressed[i]

	#end timer
	end = time.time()
	#Saving pic
	compressed_image = Image.fromarray(img_reconstruct.astype(np.uint8))
	compressed_image.save('static/compressed/'+modify_file_name(filename))

	return (round(end-start,2))

def find_pixeldiff(filename,percentage):
	img = Image.open('static/uploads/'+filename)
	m = img.size[0]
	n = img.size[1]
	k = int(math.ceil(percentage_convert(img, percentage)))
	pxdiff = ((m*k + k + k*n) / m*n) * 100
	return pxdiff

def modify_file_name(filename):
	#tanpa extension
	filename_new=""
	extension = ""
	getting_extension=False
	for i in filename:
		if (i!="." and not getting_extension):
			filename_new+=i
		elif (i=="."):
			getting_extension=True
			extension+=i
		elif (getting_extension):
			extension+=i
	return filename_new+"-compressed"+extension
