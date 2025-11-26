import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


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
    
    # Precompute constant term
    const_term = -(H * W / 2) * np.log(2 * np.pi * s ** 2)
    
    # Get background patches: (H-h+1, W-w+1, h, w)
    B_patches = sliding_window_view(B, (h, w))
    
    ll = np.zeros((H - h + 1, W - w + 1, K))
    
    for k in range(K):
        Xk = X[:, :, k]
        
        # Get all h x w patches from Xk: shape (H-h+1, W-w+1, h, w)
        patches = sliding_window_view(Xk, (h, w))
        
        # Total squared diff with background for entire image
        total_sq_diff_B = np.sum((Xk - B) ** 2)
        
        # Face region squared diff with background: (H-h+1, W-w+1)
        face_sq_diff_B = np.sum((patches - B_patches) ** 2, axis=(2, 3))
        
        # Face region squared diff with face F: (H-h+1, W-w+1)
        face_sq_diff_F = np.sum((patches - F) ** 2, axis=(2, 3))
        
        # Total squared difference for each displacement
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
    
    # Calculate log probabilities for all displacements
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)
    
    if use_MAP:
        # For MAP: q is shape (2, K) with q[0,k]=dh, q[1,k]=dw
        dh_indices = q[0, :].astype(int)
        dw_indices = q[1, :].astype(int)
        k_indices = np.arange(K)
        
        L = np.sum(log_prob[dh_indices, dw_indices, k_indices] + 
                   log_A[dh_indices, dw_indices])
    else:
        # For full posterior: q is shape (H-h+1, W-w+1, K)
        # L = sum over k, dh, dw of q * (log_prob + log_A - log_q)
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
    
    # Calculate log probabilities: log p(X_k | d_k, F, B, s)
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)
    
    # Compute unnormalized log posterior: (H-h+1, W-w+1, K)
    log_posterior = log_prob + log_A[:, :, np.newaxis]
    
    if use_MAP:
        # Return MAP estimates: shape (2, K)
        q = np.zeros((2, K))
        for k in range(K):
            idx = np.unravel_index(np.argmax(log_posterior[:, :, k]), 
                                   log_posterior[:, :, k].shape)
            q[0, k] = idx[0]  # dh
            q[1, k] = idx[1]  # dw
    else:
        # Return full posterior distribution: shape (H-h+1, W-w+1, K)
        # Use log-sum-exp trick for numerical stability
        log_posterior_max = np.max(log_posterior, axis=(0, 1), keepdims=True)
        posterior = np.exp(log_posterior - log_posterior_max)
        # Normalize over (dh, dw) for each k
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
        # q is shape (2, K)
        A = np.zeros((H - h + 1, W - w + 1))
        F_numerator = np.zeros((h, w))
        B_numerator = np.zeros((H, W))
        B_denominator = np.ones((H, W)) * K
        
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            # Update A (count occurrences)
            A[dh, dw] += 1
            
            # Update F (face region)
            F_numerator += X[dh:dh+h, dw:dw+w, k]
            
            # Update B (all pixels)
            B_numerator += X[:, :, k]
        
        # Subtract face regions from B
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            B_numerator[dh:dh+h, dw:dw+w] -= X[dh:dh+h, dw:dw+w, k]
            B_denominator[dh:dh+h, dw:dw+w] -= 1
        
        F = F_numerator / K
        B = B_numerator / np.maximum(B_denominator, 1e-10)
        A = A / K
        
        # Calculate s
        s_squared = 0.0
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            # Calculate squared error
            diff_B = X[:, :, k] - B
            s_squared += np.sum(diff_B ** 2)
            
            # Correct for face region
            diff_F_as_B = X[dh:dh+h, dw:dw+w, k] - B[dh:dh+h, dw:dw+w]
            diff_F = X[dh:dh+h, dw:dw+w, k] - F
            s_squared -= np.sum(diff_F_as_B ** 2)
            s_squared += np.sum(diff_F ** 2)
        
        s = np.sqrt(max(0, s_squared) / (K * H * W))
        
    else:
        # q is shape (H-h+1, W-w+1, K) - vectorized implementation
        
        # A: sum over K
        A = np.sum(q, axis=2) / K
        
        # Get patches from X for each k
        # X shape: (H, W, K)
        # We need patches of shape (H-h+1, W-w+1, h, w) for each k
        
        # F numerator: weighted sum of face patches
        F_numerator = np.zeros((h, w))
        B_numerator = np.zeros((H, W))
        B_denominator = np.zeros((H, W))
        
        # Total weight for F
        F_denominator = np.sum(q)
        
        for k in range(K):
            Xk = X[:, :, k]
            qk = q[:, :, k]  # (H-h+1, W-w+1)
            
            # Get patches: (H-h+1, W-w+1, h, w)
            patches = sliding_window_view(Xk, (h, w))
            
            # Weighted sum of patches for F: einsum for efficiency
            # F_numerator += sum over dh,dw of q[dh,dw,k] * patches[dh,dw,:,:]
            F_numerator += np.einsum('ij,ijkl->kl', qk, patches)
            
            # B numerator and denominator
            # For background: we accumulate weighted images and subtract face contributions
            weight_sum_k = np.sum(qk)
            B_numerator += weight_sum_k * Xk
            B_denominator += weight_sum_k
        
        # Subtract face regions from B
        # Create weight accumulator for face regions
        face_weight_acc = np.zeros((H, W))
        face_weighted_X_acc = np.zeros((H, W))
        
        for k in range(K):
            Xk = X[:, :, k]
            qk = q[:, :, k]
            
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    if qk[dh, dw] > 1e-10:
                        face_weight_acc[dh:dh+h, dw:dw+w] += qk[dh, dw]
                        face_weighted_X_acc[dh:dh+h, dw:dw+w] += qk[dh, dw] * Xk[dh:dh+h, dw:dw+w]
        
        B_numerator -= face_weighted_X_acc
        B_denominator -= face_weight_acc
        
        F = F_numerator / (F_denominator + 1e-10)
        B = B_numerator / np.maximum(B_denominator, 1e-10)
        
        # Calculate s - simplified approach
        s_squared = 0.0
        total_weight = 0.0
        
        for k in range(K):
            Xk = X[:, :, k]
            qk = q[:, :, k]
            patches = sliding_window_view(Xk, (h, w))
            B_patches = sliding_window_view(B, (h, w))
            
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    weight = qk[dh, dw]
                    if weight > 1e-10:
                        # Squared error with background (outside face)
                        total_sq = np.sum((Xk - B) ** 2)
                        # Subtract face region with background, add face region with F
                        face_sq_B = np.sum((patches[dh, dw] - B_patches[dh, dw]) ** 2)
                        face_sq_F = np.sum((patches[dh, dw] - F) ** 2)
                        
                        s_squared += weight * (total_sq - face_sq_B + face_sq_F)
                        total_weight += weight * H * W
        
        s = np.sqrt(max(0, s_squared) / (total_weight + 1e-10))
    
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
    
    # Initialize parameters if not provided
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
        # E-step: compute posterior distribution over displacements
        q = run_e_step(X, F, B, s, A, use_MAP=use_MAP)
        
        # Calculate lower bound
        L = calculate_lower_bound(X, F, B, s, A, q, use_MAP=use_MAP)
        LL.append(L)
        
        # M-step: update parameters
        F, B, s, A = run_m_step(X, q, h, w, use_MAP=use_MAP)
        
        # Check for convergence
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
        # Run EM with random initialization
        F, B, s, A, LL = run_EM(X, h, w, F=None, B=None, s=None, A=None,
                                tolerance=tolerance, max_iter=max_iter, use_MAP=use_MAP)
        
        # Get the final lower bound
        final_L = LL[-1]
        
        # Keep the best result
        if final_L > best_L:
            best_L = final_L
            best_F = F
            best_B = B
            best_s = s
            best_A = A
    
    return best_F, best_B, best_s, best_A, best_L
