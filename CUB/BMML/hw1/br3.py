import numpy as np
from scipy.signal import convolve
from scipy.stats import binom, poisson

def pa(params, model):
    range = params['amax'] - params['amin'] + 1
    p = np.full(range, 1 / range)
    val = np.arange(params['amin'], params['amax'] + 1)
    
    return p, val

def pb(params, model):
    range = params['bmax'] - params['bmin'] + 1
    p = np.full(range, 1 / (range))
    val = np.arange(params['bmin'], params['bmax'] + 1)
    return p, val

def pc(params, model):
    d = 'bin' if model == 1 else 'poiss'
    
    p_a, val_a = pa(params, model)
    p_b, val_b = pb(params, model)
    
    val_c = np.arange(0, params['amax'] + params['bmax'] + 1)
    p_c = np.zeros(len(val_c))
    
    if d == 'bin':
        a_pmfs = [binom.pmf(np.arange(a + 1), a, params['p1']) for a in val_a]
        b_pmfs = [binom.pmf(np.arange(b + 1), b, params['p2']) for b in val_b]
    
    for i, a in enumerate(val_a):
        pmf_a = a_pmfs[i] if d == 'bin' else None
        for j, b in enumerate(val_b):
            if d == 'bin':
                pmf_b = b_pmfs[j]
                conv_pmf = np.convolve(pmf_a, pmf_b, mode='full')
            else:
                lambda_sum = params['p1'] * a + params['p2'] * b
                conv_pmf = poisson.pmf(np.arange(params['amax'] + params['bmax'] + 1), lambda_sum)
            p_c[:len(conv_pmf)] += conv_pmf * p_a[i] * p_b[j]
    
    return p_c, val_c

def pd(params, model):
    val = np.arange(0, 2 * (params['amax'] + params['bmax']) + 1)
    p = np.zeros(len(val))
    p_c, _ = pc(params, model)
    for i, val_c in enumerate(p_c):
        pmf_i = binom.pmf(np.arange(i + 1), i, params['p3']) * val_c
        p[i:2 * i + 1] += pmf_i

    return p, val
        
def pc_a(a, params, model):
    d = 'bin' if model == 1 else 'poiss'
    p_b, val_b = pb(params, model)
    val_c = np.arange(0, params['amax'] + params['bmax'] + 1)
    p_c = np.zeros((len(val_c), len(a)))
    
    for i, a_val in enumerate(a):
        pmf_a = (binom.pmf(np.arange(a_val + 1), a_val, params['p1']) if d == 'bin' else poisson.pmf(np.arange(a_val + 1), params['p1'] * a_val))
        p_c_a = np.zeros(len(val_c))

        for j, b in enumerate(val_b):
            pmf_b = (binom.pmf(np.arange(b + 1), b, params['p2']) if d == 'bin' else poisson.pmf(np.arange(b + 1), params['p2'] * b))
            conv_pmf = convolve(pmf_a, pmf_b, mode='full')
            p_c_a[:len(conv_pmf)] += conv_pmf * p_b[j]
        
        p_c[:, i] = p_c_a
    
    return p_c, val_c

def pc_b(b, params, model):
    d = 'bin' if model == 1 else 'poiss'
    p_a, val_a = pa(params, model)
    val_c = np.arange(0, params['bmax'] + params['amax'] + 1)
    p_c = np.zeros((len(val_c), len(b)))
    
    for i, b_val in enumerate(b):
        pmf_b = (binom.pmf(np.arange(b_val + 1), b_val, params['p2']) if d == 'bin' else poisson.pmf(np.arange(b_val + 1), params['p2'] * b_val))
        p_c_b = np.zeros(len(val_c))

        for j, a in enumerate(val_a):
            pmf_a = (binom.pmf(np.arange(a + 1), a, params['p1']) if d == 'bin' else poisson.pmf(np.arange(a + 1), params['p1'] * a))
            conv_pmf = convolve(pmf_a, pmf_b, mode='full')
            p_c_b[:len(conv_pmf)] += conv_pmf * p_a[j]
        
        p_c[:, i] = p_c_b

    return p_c, val_c   

def pd_c(c, params, model):
    cmax = (params['amax'] + params['bmax'])
    vals = np.arange(2 * cmax + 1)
    p = binom.pmf(vals[:, None] - c[None, :], c, params['p3'])
    return p, vals

def pc_d(d, params, model):
    p_c, val = pc(params, model)
    pd_c_p, _ = pd_c(val, params, model)
    num = (pd_c_p[d, :] * p_c).transpose(1, 0)
    p = num / num.sum(axis=0)
    return p, val
    
def pc_ab(a, b, params, model):
    val = np.arange(0, params['amax'] + params['bmax'] + 1)
    max_conv = params['amax'] + params['bmax'] + 1
    p = np.zeros((max_conv, len(a), len(b)))
    d = 'bin' if model == 1 else 'poiss' if model == 2 else None
    pmf_X = [binom.pmf(np.arange(a_i + 1), a_i, params['p1']) if d == 'bin' else poisson.pmf(np.arange(a_i + 1), params['p1'] * a_i) for a_i in a]
    pmf_Y = [binom.pmf(np.arange(b_j + 1), b_j, params['p2']) if d == 'bin' else poisson.pmf(np.arange(b_j + 1), params['p2'] * b_j) for b_j in b]
    
    for i, pmf_x in enumerate(pmf_X):
        for j, pmf_y in enumerate(pmf_Y):
            if d == 'bin':
                conv_pmf = convolve(pmf_x, pmf_y, mode='full')
                p[:len(conv_pmf), i, j] = conv_pmf
            else:
                lambda_sum = params['p1'] * a[i] + params['p2'] * b[j]
                max_k = len(pmf_x) + len(pmf_y) - 1
                p[:max_k, i, j] = poisson.pmf(np.arange(max_k), lambda_sum)

    return p, val
    
def pc_abd(a, b, d, params, model):
    p_c_ab, val = pc_ab(a, b, params, model)
    p_c, _ = pd_c(val, params, model)
    p_d_c = p_c[d, :]
    num = np.diagonal(np.tensordot(p_d_c, p_c_ab, axes=0), axis1=1, axis2=2).transpose(3, 1, 2, 0)
    p = num / num.sum(axis=0)
    return p, val   