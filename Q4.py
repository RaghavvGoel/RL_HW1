#!/usr/bin/env python
import numpy as np
import pdb 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import sys
import math


def action_value(step_sz, eps, switch , q_star, total_steps, runs):
	N = 10
	# total_steps = 1000
	# runs = 5000
	Opt_a = np.zeros(total_steps)
	R_f = np.zeros(total_steps)

	for i in range(runs):

		step = 0;
		
		q_star = np.random.normal(0, 1, N) #np.ones(N)
		if switch == 0:
			Q = 5*np.ones(N)
		else:
			Q = np.zeros(N)		
		R = np.zeros(total_steps)

		#eps = 0.1;
		#step_sz = 1.0/total_steps

		while step < total_steps:

			#pdb.set_trace()
			#q_star = q_star + np.random.normal(0, 0.01, N)

			p = np.random.rand(1)
			if p[0] < eps: #explore
				p2 = np.random.rand(1)[0]
				a = int(np.floor(p2*10))
				#R[step] = Q[a]
			else:
				a = np.argmax(Q)
				#R[step] = Q[a]

			if a == np.argmax(q_star):
				Opt_a[step] += 1;	

			R[step] = np.random.normal(q_star[a],1, 1)	
			Q[a] = Q[a] + step_sz*(R[step] - Q[a])

			
			step += 1;

		#addding all the rewards	
		R_f += R
		print("run completed = " , i)

	R_f = R_f/runs
	Opt_a = Opt_a/runs

	return R_f, Opt_a

def action_value_UCB(runs, total_steps, step_sz):

	N = 10
	c = 2;
	Opt_a = np.zeros(total_steps)
	R_f = np.zeros(total_steps)

	for i in range(runs):

		q_star = np.random.normal(0, 1, N)#np.ones(N)
		Q = np.zeros(N)
		step = 0;

		R = np.zeros(total_steps)
		noa = np.ones(N)

		while step < total_steps:

			#pdb.set_trace()
			#q_star = q_star + np.random.normal(0, 0.01, N)

			a = np.argmax(Q + c*np.power(np.log(step+1)/(noa) , 0.5))
			noa[a] += 1
			# if a == np.argmax(q_star):
			# 	Opt_a[step] += 1;	

			R[step] = np.random.normal(q_star[a],1, 1)	
			Q[a] = Q[a] + step_sz*(R[step] - Q[a])

			
			step += 1;

		#addding all the rewards	
		R_f += R
		print("run completed = " , i)

	R_f = R_f/runs
	Opt_a = Opt_a/runs

	return R_f		



R = []
OA = []

N = 10
total_steps = 1000
runs = 2000
step_sz = 0.1
R3 = action_value_UCB(runs, total_steps, step_sz)
R.append(R3)


step_sz = 0.1#1.0/total_steps
q_star = np.ones(N)

eps = 0
Q = 5*np.ones(N)
R1, oa1 = action_value(step_sz, eps, 0 ,q_star, total_steps, runs)
R.append(R1)
OA.append(oa1)

#pdb.set_trace()

eps = 0.1
Q = np.zeros(N)
R2, oa2 = action_value(step_sz, eps, 1 ,q_star, total_steps, runs)
R.append(R2)
OA.append(oa2)


X = np.arange(total_steps) #[i for i in range(t)]

C = ('green', 'blue' , 'red')
label = ('UCB' , 'Optimistic,greedy' , 'Realistic,e-greedy')
#plt.plot(X, np.random(10, size=t))
line_label = []	
lines = []
for j in range(3):
	lines.append(plt.plot(X, R[j], color=C[j]))
	line_label.append(label[j])

plt.legend(line_label)
plt.ylabel('Average Reward' , size=10)
plt.xlabel('Steps', size=10)
plt.title("Stationary")
plt.show()	

# line_label = []	
# lines = []
# for j in range(2):
# 	lines.append(plt.plot(X, OA[j], color=C[j]))
# 	line_label.append(label[j])

# plt.legend(line_label)
# plt.ylabel('Optimal Action' , size=10)
# plt.xlabel('Steps', size=10)
# plt.title("Non Stationary q_star")
# plt.show()