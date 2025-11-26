import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from scipy.signal import fftconvolve


def calculate_log_probability(X, F, B, s):
    """
    Calculates log p(X_k|d_k,F,B,s) for all images X_k in X and
    all possible displacements d_k.

    Parameters
    ----------
    X : array, shape (H, W, K)
        K images of size H x W.
    F : array, shape (h, w)
        Estimate of villain's face.
    B : array, shape (H, W)
        Estimate of background.
    s : float
        Estimate of standard deviation of Gaussian noise.

    Returns
    -------
    ll : array, shape(H-h+1, W-w+1, K)
        ll[dh,dw,k] - log-likelihood of observing image X_k given
        that the villain's face F is located at displacement (dh, dw)
    """
    H, W, K = X.shape
    h, w = F.shape
    
    const_term = -(H * W / 2) * np.log(2 * np.pi * s ** 2)
    
    B_patches = sliding_window_view(B, (h, w))
    
    ll = np.zeros((H - h + 1, W - w + 1, K))
    
    for k in range(K):
        Xk = X[:, :, k]
        
        patches = sliding_window_view(Xk, (h, w))
        
        total_sq_diff_B = np.sum((Xk - B) ** 2)
        
        face_sq_diff_B = np.sum((patches - B_patches) ** 2, axis=(2, 3))
        
        face_sq_diff_F = np.sum((patches - F) ** 2, axis=(2, 3))
        
        sq_diff = total_sq_diff_B - face_sq_diff_B + face_sq_diff_F
        
        ll[:, :, k] = -sq_diff / (2 * s ** 2) + const_term
    
    return ll


def calculate_lower_bound(X, F, B, s, A, q, use_MAP=False):
    """
    Calculates the lower bound L(q,F,B,s,A) for the marginal log likelihood.

    Parameters
    ----------
    X : array, shape (H, W, K)
        K images of size H x W.
    F : array, shape (h, w)
        Estimate of villain's face.
    B : array, shape (H, W)
        Estimate of background.
    s : float
        Estimate of standard deviation of Gaussian noise.
    A : array, shape (H-h+1, W-w+1)
        Estimate of prior on displacement of face in any image.
    q : array
        If use_MAP = False: shape (H-h+1, W-w+1, K)
            q[dh,dw,k] - estimate of posterior of displacement (dh,dw)
            of villain's face given image Xk
        If use_MAP = True: shape (2, K)
            q[0,k] - MAP estimates of dh for X_k
            q[1,k] - MAP estimates of dw for X_k
    use_MAP : bool, optional
        If true then q is a MAP estimates of displacement (dh,dw) of
        villain's face given image Xk.

    Returns
    -------
    L : float
        The lower bound L(q,F,B,s,A) for the marginal log likelihood.
    """
    H, W, K = X.shape
    h, w = F.shape
    
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)
    
    if use_MAP:
        dh_indices = q[0, :].astype(int)
        dw_indices = q[1, :].astype(int)
        k_indices = np.arange(K)
        
        L = np.sum(log_prob[dh_indices, dw_indices, k_indices] + 
                   log_A[dh_indices, dw_indices])
    else:
        mask = q > 1e-10
        L = np.sum(q[mask] * (log_prob[mask] + log_A[:, :, np.newaxis].repeat(K, axis=2)[mask] 
                              - np.log(q[mask])))
    
    return L


def run_e_step(X, F, B, s, A, use_MAP=False):
    """
    Given the current esitmate of the parameters, for each image Xk
    esitmates the probability p(d_k|X_k,F,B,s,A).

    Parameters
    ----------
    X : array, shape(H, W, K)
        K images of size H x W.
    F  : array_like, shape(h, w)
        Estimate of villain's face.
    B : array shape(H, W)
        Estimate of background.
    s : scalar, shape(1, 1)
        Eestimate of standard deviation of Gaussian noise.
    A : array, shape(H-h+1, W-w+1)
        Estimate of prior on displacement of face in any image.
    use_MAP : bool, optional,
        If true then q is a MAP estimates of displacement (dh,dw) of
        villain's face given image Xk.

    Returns
    -------
    q : array
        If use_MAP = False: shape (H-h+1, W-w+1, K)
            q[dh,dw,k] - estimate of posterior of displacement (dh,dw)
            of villain's face given image Xk
        If use_MAP = True: shape (2, K)
            q[0,k] - MAP estimates of dh for X_k
            q[1,k] - MAP estimates of dw for X_k
    """
    H, W, K = X.shape
    h, w = F.shape
    
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)
    
    log_posterior = log_prob + log_A[:, :, np.newaxis]
    
    if use_MAP:
        q = np.zeros((2, K))
        for k in range(K):
            idx = np.unravel_index(np.argmax(log_posterior[:, :, k]), 
                                   log_posterior[:, :, k].shape)
            q[0, k] = idx[0]  # dh
            q[1, k] = idx[1]  # dw
    else:
        log_posterior_max = np.max(log_posterior, axis=(0, 1), keepdims=True)
        posterior = np.exp(log_posterior - log_posterior_max)
        q = posterior / np.sum(posterior, axis=(0, 1), keepdims=True)
    
    return q


def run_m_step(X, q, h, w, use_MAP=False):
    """
    Estimates F,B,s,A given esitmate of posteriors defined by q.

    Parameters
    ----------
    X : array, shape(H, W, K)
        K images of size H x W.
    q  :
        if use_MAP = False: array, shape (H-h+1, W-w+1, K)
           q[dh,dw,k] - estimate of posterior of displacement (dh,dw)
           of villain's face given image Xk
        if use_MAP = True: array, shape (2, K)
            q[0,k] - MAP estimates of dh for X_k
            q[1,k] - MAP estimates of dw for X_k
    h : int
        Face mask height.
    w : int
        Face mask width.
    use_MAP : bool, optional
        If true then q is a MAP estimates of displacement (dh,dw) of
        villain's face given image Xk.

    Returns
    -------
    F : array, shape (h, w)
        Estimate of villain's face.
    B : array, shape (H, W)
        Estimate of background.
    s : float
        Estimate of standard deviation of Gaussian noise.
    A : array, shape (H-h+1, W-w+1)
        Estimate of prior on displacement of face in any image.
    """
    H, W, K = X.shape
    
    if use_MAP:
        A = np.zeros((H - h + 1, W - w + 1))
        F_numerator = np.zeros((h, w))
        B_numerator = np.zeros((H, W))
        B_denominator = np.ones((H, W)) * K
        
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            A[dh, dw] += 1
            
            F_numerator += X[dh:dh+h, dw:dw+w, k]
            
            B_numerator += X[:, :, k]
        
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            B_numerator[dh:dh+h, dw:dw+w] -= X[dh:dh+h, dw:dw+w, k]
            B_denominator[dh:dh+h, dw:dw+w] -= 1
        
        F = F_numerator / K
        B = B_numerator / np.maximum(B_denominator, 1e-10)
        A = A / K
        
        s_squared = 0.0
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            diff_B = X[:, :, k] - B
            s_squared += np.sum(diff_B ** 2)
            
            diff_F_as_B = X[dh:dh+h, dw:dw+w, k] - B[dh:dh+h, dw:dw+w]
            diff_F = X[dh:dh+h, dw:dw+w, k] - F
            s_squared -= np.sum(diff_F_as_B ** 2)
            s_squared += np.sum(diff_F ** 2)
        
        s = np.sqrt(max(0, s_squared) / (K * H * W))
        
    else:
        A = np.sum(q, axis=2) / K
        
        F = np.zeros((h, w))
        for k in range(K):
            patches = sliding_window_view(X[:, :, k], (h, w))
            F += np.einsum('ij,ijkl->kl', q[:, :, k], patches)
        F = F / K
        
        kernel = np.ones((h, w))
        face_weight = np.zeros((H, W))
        face_weighted_X = np.zeros((H, W))
        
        for k in range(K):
            qk_conv = fftconvolve(q[:, :, k], kernel, mode='full')[:H, :W]
            face_weight += qk_conv
            face_weighted_X += X[:, :, k] * qk_conv
        
        B_num = np.sum(X, axis=2) - face_weighted_X
        B_den = K - face_weight
        B = np.divide(B_num, B_den, out=np.zeros_like(B_num), where=B_den > 0)
        
        B_patches = sliding_window_view(B, (h, w))
        s_squared = 0.0
        for k in range(K):
            Xk = X[:, :, k]
            qk = q[:, :, k]
            patches = sliding_window_view(Xk, (h, w))
            
            total_sq_B = np.sum((Xk - B) ** 2)
            face_sq_B = np.sum((patches - B_patches) ** 2, axis=(2, 3))
            face_sq_F = np.sum((patches - F) ** 2, axis=(2, 3))
            
            s_squared += np.sum(qk * (total_sq_B - face_sq_B + face_sq_F))
        
        s = np.sqrt(max(0, s_squared) / (K * H * W))
    
    return F, B, s, A


def run_EM(X, h, w, F=None, B=None, s=None, A=None, tolerance=0.001,
           max_iter=50, use_MAP=False):
    """
    Runs EM loop until the likelihood of observing X given current
    estimate of parameters is idempotent as defined by a fixed
    tolerance.

    Parameters
    ----------
    X : array, shape (H, W, K)
        K images of size H x W.
    h : int
        Face mask height.
    w : int
        Face mask width.
    F : array, shape (h, w), optional
        Initial estimate of villain's face.
    B : array, shape (H, W), optional
        Initial estimate of background.
    s : float, optional
        Initial estimate of standard deviation of Gaussian noise.
    A : array, shape (H-h+1, W-w+1), optional
        Initial estimate of prior on displacement of face in any image.
    tolerance : float, optional
        Parameter for stopping criterion.
    max_iter  : int, optional
        Maximum number of iterations.
    use_MAP : bool, optional
        If true then after E-step we take only MAP estimates of displacement
        (dh,dw) of villain's face given image Xk.

    Returns
    -------
    F, B, s, A : trained parameters.
    LL : array, shape(number_of_iters,)
        L(q,F,B,s,A) after each EM iteration (1 iteration = 1 e-step + 1 m-step); 
        number_of_iters is actual number of iterations that was done.
    """
    H, W, K = X.shape
    
    if F is None:
        F = np.random.rand(h, w)
    if B is None:
        B = np.random.rand(H, W)
    if s is None:
        s = 1.0
    if A is None:
        A = np.ones((H - h + 1, W - w + 1))
        A = A / np.sum(A)
    
    LL = []
    
    for iteration in range(max_iter):
        q = run_e_step(X, F, B, s, A, use_MAP=use_MAP)
        
        F, B, s, A = run_m_step(X, q, h, w, use_MAP=use_MAP)
        
        L = calculate_lower_bound(X, F, B, s, A, q, use_MAP=use_MAP)
        LL.append(L)
        
        if iteration > 0 and abs(LL[-1] - LL[-2]) < tolerance:
            break
    
    return F, B, s, A, np.array(LL)


def run_EM_with_restarts(X, h, w, tolerance=0.001, max_iter=50, use_MAP=False,
                         n_restarts=10):
    """
    Restarts EM several times from different random initializations
    and stores the best estimate of the parameters as measured by
    the L(q,F,B,s,A).

    Parameters
    ----------
    X : array, shape (H, W, K)
        K images of size H x W.
    h : int
        Face mask height.
    w : int
        Face mask width.
    tolerance, max_iter, use_MAP : optional parameters for EM.
    n_restarts : int
        Number of EM runs.

    Returns
    -------
    F : array,  shape (h, w)
        The best estimate of villain's face.
    B : array, shape (H, W)
        The best estimate of background.
    s : float
        The best estimate of standard deviation of Gaussian noise.
    A : array, shape (H-h+1, W-w+1)
        The best estimate of prior on displacement of face in any image.
    L : float
        The best L(q,F,B,s,A).
    """
    best_L = -np.inf
    best_F = None
    best_B = None
    best_s = None
    best_A = None
    
    for restart in range(n_restarts):
        F, B, s, A, LL = run_EM(X, h, w, F=None, B=None, s=None, A=None,
                                tolerance=tolerance, max_iter=max_iter, use_MAP=use_MAP)
        
        final_L = LL[-1]
        
        if final_L > best_L:
            best_L = final_L
            best_F = F
            best_B = B
            best_s = s
            best_A = A
    
    return best_F, best_B, best_s, best_A, best_L

