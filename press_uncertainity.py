import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
from scipy.stats import sem
import scipy.stats as stats
import math
from lmfit import Model
from pymatgen.core.periodic_table import Element
from scipy import constants as const
from matplotlib import rc
from statistics import mean

vol, press, press2, pres_std, pres_ci = [],[],[],[], []
press2 = []
press = []
#press = open("cp2k_38Flinazr_lx.txt","r")

with open('cp2k_38Flinazr_lx.txt', 'r') as f:
    next(f) # discard the first line
    press2 = [line for line in f]   # save numbers to a list
for element in press2:
    press.append(float(element.strip('\n')))
z_critical = stats.norm.ppf(q = 0.95)

# print(press2[14275], press[14275])
# print(len(press))

# skip_steps = 10000
# extfile = os.path.join(d, 'extract.pkl')
# data = pickle.load(open(extfile, 'rb'))
# p_std = sem(data['pressure(kB)'][skip_steps:])

p_mean = np.mean(press)

# PERFORM covariance analyiss
# press = data['total pressure'][skip_steps:]
n = len(press)
kmax = int(np.round(np.sqrt(n)))

gk_sum = 0
for k in range(kmax):
    p1 = press[k:]
    p2 = press[:len(p1)]
    gk = np.cov(p1, p2)[1,1]
    if k==0:
        assert (np.array_equal(p1, p2))
        g0 = gk
    else:
        gk_sum += (n-k)/n*gk
var_m = 1/n*(g0 + 2*gk_sum)
p_std = 2*np.sqrt(var_m)
press.append(p_mean)
pres_std.append(p_std)
margin_of_error = z_critical*(p_std/math.sqrt(len(press)))
pres_ci.append(margin_of_error)

print(p_std)
print(pres_ci)

'''
data = np.column_stack([p_std])
datafile_path = "press_uncertainity.txt"
np.savetxt(datafile_path , data)
'''
