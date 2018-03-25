import numpy as np
from skimage.transform import rescale
from scipy import sparse
from scipy.interpolate import griddata, NearestNDInterpolator, interp2d, LinearNDInterpolator, RegularGridInterpolator, Rbf
import matplotlib.pyplot as plt
import time

R = []

# @inproceedings{ma2016sparse,
#   title={Sparse sensing for resource-constrained depth reconstruction},
#   author={Ma, Fangchang and Carlone, Luca and Ayaz, Ulas and Karaman, Sertac},
#   booktitle={Intelligent Robots and Systems (IROS), 2016 IEEE/RSJ International Conference on},
#   pages={96--103},
#   year={2016},
#   organization={IEEE}
# }

# @article{Ma2017SparseDepthSensing,
#   title={Sparse Depth Sensing for Resource-Constrained Robots},
#   author={Ma, Fangchang and Carlone, Luca and Ayaz, Ulas and Karaman, Sertac},
#   journal={arXiv preprint arXiv:1703.01398},
#   year={2017}
# }

# def Perform_TV_Constraint(xk,mu,D):
# 	Dx = D*xk
# 	tvx = abs(Dx)
# 	tvx[tvx < mu] = mu
# 	u = Dx / tvx
# 	fx = np.real(np.matmul(u.T, Dx) - mu/2 * np.matmul(u.T, u)/u.size)
# 	df = D.T*u

# 	return df, fx


# def my_Core_Nesterov(b,mu,delta,opts):
# 	xk = xplug = opts['xplug']
# 	D = opts['D']
# 	samples = opts['samples']
# 	TolVar = opts['TolVar']
# 	maxiter = opts['maxiter']

# 	N = len(xplug)
# 	wk = np.zeros(N)
# 	Lmu = 32*(1**(2/mu))
# 	yk = xk
# 	zk = xk

# 	fmean = 1/np.finfo(np.float).max
# 	OK = False
# 	n = np.floor(np.sqrt(N))

# 	A_xk = A_xk_c = R*xk

# 	#  for linf norm
# 	bm = b-delta
# 	bp = b+delta

	

# 	for k in range(maxiter):
# 		if k % 1000 == 0:
# 			print(k)

# 		df, fx = Perform_TV_Constraint(xk,mu,D)
# 		yk = xk - df/Lmu

# 		yks = yk[samples]
# 		np.where(yks < bm, yk[samples], bm)
# 		np.where(yks < bp, yk[samples], bp)

# 		A_yk = yk[samples]
        
# 		qp = abs(fx - np.mean(fmean))/np.mean(fmean)


# 		if qp <= TolVar and OK:
# 			break
# 		if qp <= TolVar and ~OK:
# 			OK = True

# 		fmean = np.hstack((fx, fmean))

# 		if (len(fmean) > 10):
# 			fmean = fmean[0:10]

# 		alpha_k = 0.5*(k+1)
# 		tau_k = 2./(k+3)
# 		wk =  alpha_k*df + wk
        
# 		zk = xplug - wk/Lmu

# 		zks = zk[samples]
# 		np.where(zks < bm, zk[samples], bm)
# 		np.where(zks < bp, zk[samples], bp)

# 		Azk = zk[samples]

# 		xk = tau_k*zk + (1-tau_k)*yk
# 		A_xk = tau_k*Azk + (1-tau_k)*A_yk

# 		if k % 9 == 0 and k != 0:
# 			A_xk = A_xk_c

# 	return xk

# def myNESTA(b,muf,delta,opts):

# 	xplug = opts['xplug']
# 	MaxIntIter = opts['MaxIntIter']
# 	TolVar = opts['TolVar']

# 	mu0 = max(abs(opts['D'] * xplug))
# 	Gamma = (muf/mu0)**(1./MaxIntIter)
# 	mu = mu0
# 	Gammat = (TolVar/0.1)**(1./MaxIntIter)
# 	TolVar = 0.1

# 	for nl in range(MaxIntIter):
# 		print(nl)
# 		mu = mu*Gamma
# 		TolVar = TolVar*Gammat 
# 		opts['TolVar'] = TolVar
# 		opts['xplug'] = xplug

# 		xk = my_Core_Nesterov(b,mu,delta,opts)    
# 		xplug = xk
	    
# 	return xk


# def solve_nesta_2D(TV2,y,samples,epsilon,xInit,mu):
# 	opts = {}

# 	opts['TolVar'] = 1e-6
# 	opts['D'] = TV2
# 	opts['maxiter'] = 10000
# 	opts['xplug'] = xInit
# 	opts['samples'] = samples
# 	opts['MaxIntIter'] = 3

# 	zFast = myNESTA(y,mu,epsilon,opts)

# 	return zFast


# def createFiniteDiff2(Nx,Ny):
# 	indptrx = np.arange(0, 3*Nx-5, 3)
# 	x = np.array([0,1,2])
# 	indicesx = np.array([])
# 	for i in range(len(indptrx)-1):
# 		indicesx = np.concatenate((indicesx, x))
# 		x = x+1
# 	datax = np.tile([1,-2,1], Nx-2)
# 	V = sparse.csr_matrix((datax, indicesx, indptrx), shape=(Nx-2, Nx))

# 	indptry = np.arange(0, 3*Ny-5, 3)
# 	y = np.array([0,1,2])
# 	indicesy = np.array([])
# 	for i in range(len(indptry)-1):
# 		indicesy = np.concatenate((indicesy, y))
# 		y = y+1
# 	datay = np.tile([1,-2,1], Ny-2)
# 	H = sparse.csc_matrix((datay, indicesy, indptry), shape=(Ny, Ny-2))

# 	return H, V

# def l1ReconstructionOnImage(height, width, y, settings, samples, zinit):
# 	H,V = createFiniteDiff2(height, width)
# 	TV2_V = sparse.kron(sparse.eye(width), V)
# 	TV2_H = sparse.kron(H.T, sparse.eye(height))
# 	TV2 = sparse.vstack([TV2_V, TV2_H])
# 	z = solve_nesta_2D(TV2, y, samples, 0, zinit, 0.001)
# 	return z.reshape((height, width))








def createSamples(depth, rgb, settings):
	height = depth.shape[0]
	width = depth.shape[1]
	N = height * width
	K = int(N * settings['perc_samples'])
	rand = np.random.permutation(N)[:K]

	a = np.isnan(depth.flatten()[rand])
	samples = rand[np.nonzero(~a)[0]]
	print("Percentage samples taken: ", len(samples))

	return samples

def getRawData(settings, n):
	npzfile = np.load('npz/%d_c_5d.npz' % n)
	rgb = npzfile['arr_0']

	depth = np.float16(npzfile['arr_1'])

	depth[depth <= 0] = np.nan
	depth[depth > 4000] = np.nan

	for i in range(settings['frames'] -1):
		s = 'arr_%d' % (i+2)
		curr = np.float16(npzfile[s])
		curr[curr <= 0] = np.nan
		curr[curr > 4000] = np.nan
		depth = np.dstack((depth, curr))

	depth = np.nanmean(depth, 2)/1000
	depth[depth <= 0] = np.nan
	depth[depth > 4000] = np.nan

	if settings['sub_sample'] < 1:
		depth = rescale(depth, settings['sub_sample'])
		# rgb = rescale(rgb, settings['sub_sample'])

	return (depth, rgb)

def linearInterpolationOnImage(settings, height, width, samples, measured_vector):
	
	h = np.arange(0, height)
	w = np.arange(0, width)

	Yq, Zq = np.meshgrid(w, h)
	Y_sample = Yq.flatten()[samples]
	Z_sample = Zq.flatten()[samples]
	points = np.column_stack((Y_sample,Z_sample))

	fn = NearestNDInterpolator(points, measured_vector)
	NNDI = fn(Yq, Zq)

	fl = LinearNDInterpolator(points, measured_vector)
	LNDI = fl(Yq, Zq)

	GD = griddata(points, measured_vector, (Yq, Zq), method=settings['method'])

	rbf1 = Rbf(Y_sample, Z_sample, measured_vector, function='linear')
	RBF1 = rbf1(Yq, Zq)

	rbf2 = Rbf(Y_sample, Z_sample, measured_vector, function='thin_plate')
	RBF2 = rbf2(Yq, Zq)

	rbf3 = Rbf(Y_sample, Z_sample, measured_vector, function='cubic')
	RBF3 = rbf3(Yq, Zq)

	rbf4 = Rbf(Y_sample, Z_sample, measured_vector, function='multiquadric')
	RBF4 = rbf4(Yq, Zq)


	return GD, NNDI, LNDI, RBF1, RBF2, RBF3, RBF4

def reconstructDepthImage(settings, height, width, measured_vector, samples):
	x = linearInterpolationOnImage(settings, height, width, samples, measured_vector)
	# z = l1ReconstructionOnImage(height, width, measured_vector, settings, samples, x[1].flatten())
	z = x[1]
	return x, z


def plot(cmap, rgb, depth, depth_sampled, x):
	plt.subplot(4, 4, 1)
	plt.title('RGB')
	plt.imshow(rgb)
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 2)
	plt.imshow(depth, cmap=cmap)
	plt.title('Original')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 3)
	plt.imshow(depth_sampled, cmap=cmap)
	plt.title('depth_sample')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 4)
	plt.imshow(x[0], cmap=cmap)
	plt.title('GridData')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 5)
	plt.imshow(x[1], cmap=cmap)
	plt.title('NNDI')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 6)
	plt.imshow(x[2], cmap=cmap)
	plt.title('LNDI')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	# plt.subplot(4, 4, 7)
	# plt.imshow(x[7], cmap=cmap)
	# plt.title('')
	# plt.xticks(visible=False)
	# plt.yticks(visible=False)

	plt.subplot(4, 4, 8)
	plt.imshow(x[3], cmap=cmap)
	plt.title('rbf1')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 9)
	plt.imshow(x[4], cmap=cmap)
	plt.title('rbf2')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 10)
	plt.imshow(x[5], cmap=cmap)
	plt.title('rbf3')
	plt.xticks(visible=False)
	plt.yticks(visible=False)

	plt.subplot(4, 4, 11)
	plt.imshow(x[6], cmap=cmap)
	plt.title('rbf4')
	plt.xticks(visible=False)
	plt.yticks(visible=False)


	plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)
	cax = plt.axes([0.85, 0.1, 0.075, 0.8])
	plt.colorbar(cax=cax)

	plt.show()


def reconstruct_single_frame(settings, n):
	t = time.time()
	depth, rgb = getRawData(settings, n)
	print("Number of abailable values: ", np.count_nonzero(np.isnan(depth)))

	samples = createSamples(depth, rgb, settings)
	
	xGT = depth.flatten()
	N = len(xGT)

	height = depth.shape[0]
	width = depth.shape[1]

	Rfull = sparse.eye(N)
	global R
	R = Rfull.tocsr()[samples,:]
	measured_vector = R*xGT

	mask = np.ones(len(xGT), np.bool)
	mask[samples] = 0
	xGT[mask] = np.nan
	depth_sampled = xGT.reshape(height,width)

	x = reconstructDepthImage(settings, height, width, measured_vector, samples)
	obstacleAvoid(x[3])

	print("time:", time.time() - t)

	if settings['plot']:
		plot(settings['cmap'], rgb, depth, depth_sampled, x)


def find_largest_gap(collisions):
	lmax = 0
	f = 0
	lcurr = 0
	past = False
	for i, val in enumerate(collisions):
		if (val == -1):
			if (past == False):
				lcurr = 1
				past = True
			else:
				lcurr = lcurr + 1

		else:
			if(past == True):
				past = False
				if (lmax < lcurr):
					lmax = lcurr
					f = i - 1
				lcurr =0

	if(past == True and lmax < lcurr):
		lmax = lcurr
		f = i - 1
	print(lmax, f)
	return (f - lmax/2)

def obstacleAvoid(depth):
  	max_dist = 1
  	depth[depth > max_dist] = -1
  	d = depth[-1,:]
  	angle_swept = 60
  	a = find_largest_gap(d)
  	rot = 1.0*a*angle_swept/len(d) - angle_swept/2.

  	print("Rotate {:.1f}degrees".format(rot))
  	# print(a)

def main():
	settings = {}

	settings['cmap'] = 'gray' #gray, rainbow, winter, spring, autumn
	settings['sub_sample'] = 0.3
	settings['perc_samples'] = 0.03
	settings['method'] = 'cubic'
	settings['frames'] = 5
	settings['plot'] = True

	reconstruct_single_frame(settings, 2)
	return

if __name__== "__main__":
  main()


