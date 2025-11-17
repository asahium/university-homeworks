
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
    import numpy as np
    
    H, W, K = X.shape
    h, w = F.shape
    
    ll = np.zeros((H - h + 1, W - w + 1, K))
    
    # For each image
    for k in range(K):
        # For each possible displacement
        for dh in range(H - h + 1):
            for dw in range(W - w + 1):
                # Create the expected image: background + face at position (dh, dw)
                expected = np.copy(B)
                expected[dh:dh+h, dw:dw+w] = F
                
                # Calculate Gaussian log-likelihood
                # log p(X|expected, s) = -0.5 * sum((X - expected)^2) / s^2 - n/2 * log(2*pi*s^2)
                diff = X[:, :, k] - expected
                ll[dh, dw, k] = -np.sum(diff ** 2) / (2 * s ** 2) - (H * W / 2) * np.log(2 * np.pi * s ** 2)
    
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
    import numpy as np
    
    H, W, K = X.shape
    h, w = F.shape
    
    # Calculate log probabilities for all displacements
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)  # Add small epsilon to avoid log(0)
    
    L = 0.0
    
    if use_MAP:
        # For MAP: q is shape (2, K) with q[0,k]=dh, q[1,k]=dw
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            # L += log p(X_k | d_k, F, B, s) + log p(d_k | A)
            L += log_prob[dh, dw, k] + log_A[dh, dw]
    else:
        # For full posterior: q is shape (H-h+1, W-w+1, K)
        for k in range(K):
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    if q[dh, dw, k] > 1e-10:
                        # L += q * (log p(X_k | d_k, F, B, s) + log p(d_k | A) - log q)
                        L += q[dh, dw, k] * (log_prob[dh, dw, k] + log_A[dh, dw] - np.log(q[dh, dw, k]))
    
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
    import numpy as np
    
    H, W, K = X.shape
    h, w = F.shape
    
    # Calculate log probabilities: log p(X_k | d_k, F, B, s)
    log_prob = calculate_log_probability(X, F, B, s)
    log_A = np.log(A + 1e-10)
    
    if use_MAP:
        # Return MAP estimates: shape (2, K)
        q = np.zeros((2, K))
        for k in range(K):
            # Compute unnormalized log posterior
            log_posterior = log_prob[:, :, k] + log_A
            # Find MAP estimate
            idx = np.unravel_index(np.argmax(log_posterior), log_posterior.shape)
            q[0, k] = idx[0]  # dh
            q[1, k] = idx[1]  # dw
    else:
        # Return full posterior distribution: shape (H-h+1, W-w+1, K)
        q = np.zeros((H - h + 1, W - w + 1, K))
        for k in range(K):
            # Compute unnormalized log posterior: log p(X_k | d_k, F, B, s) + log p(d_k | A)
            log_posterior = log_prob[:, :, k] + log_A
            # Convert to probabilities using log-sum-exp trick for numerical stability
            log_posterior_max = np.max(log_posterior)
            posterior = np.exp(log_posterior - log_posterior_max)
            # Normalize
            q[:, :, k] = posterior / np.sum(posterior)
    
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
    import numpy as np
    
    H, W, K = X.shape
    
    # Initialize parameters
    F_numerator = np.zeros((h, w))
    F_denominator = 0.0
    B_numerator = np.zeros((H, W))
    B_denominator = np.zeros((H, W))
    A = np.zeros((H - h + 1, W - w + 1))
    
    if use_MAP:
        # q is shape (2, K)
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            # Update A (count occurrences)
            A[dh, dw] += 1
            
            # Update F (face region)
            F_numerator += X[dh:dh+h, dw:dw+w, k]
            F_denominator += 1
            
            # Update B (all pixels, we'll subtract face contribution)
            B_numerator += X[:, :, k]
            B_denominator += 1
        
        # Subtract face regions from B
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            B_numerator[dh:dh+h, dw:dw+w] -= X[dh:dh+h, dw:dw+w, k]
            B_denominator[dh:dh+h, dw:dw+w] -= 1
    else:
        # q is shape (H-h+1, W-w+1, K)
        # Sum A over K
        A = np.sum(q, axis=2)
        
        for k in range(K):
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    weight = q[dh, dw, k]
                    if weight > 1e-10:
                        # Update F (weighted average of face regions)
                        F_numerator += weight * X[dh:dh+h, dw:dw+w, k]
                        F_denominator += weight
                        
                        # Update B (all pixels weighted)
                        B_numerator += weight * X[:, :, k]
                        B_denominator += weight
        
        # Subtract face regions from B
        for k in range(K):
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    weight = q[dh, dw, k]
                    if weight > 1e-10:
                        B_numerator[dh:dh+h, dw:dw+w] -= weight * X[dh:dh+h, dw:dw+w, k]
                        B_denominator[dh:dh+h, dw:dw+w] -= weight
    
    # Finalize F and B
    F = F_numerator / (F_denominator + 1e-10)
    B = B_numerator / (B_denominator + 1e-10)
    
    # Normalize A
    A = A / K
    
    # Calculate s (standard deviation) - reuse logic from before
    s_squared = 0.0
    total_weight = 0.0
    
    if use_MAP:
        for k in range(K):
            dh = int(q[0, k])
            dw = int(q[1, k])
            
            # Calculate squared error for background
            diff_B = X[:, :, k] - B
            s_squared += np.sum(diff_B ** 2)
            
            # Correct for face region
            diff_F_as_B = X[dh:dh+h, dw:dw+w, k] - B[dh:dh+h, dw:dw+w]
            diff_F = X[dh:dh+h, dw:dw+w, k] - F
            s_squared -= np.sum(diff_F_as_B ** 2)
            s_squared += np.sum(diff_F ** 2)
            
            total_weight += H * W
    else:
        for k in range(K):
            for dh in range(H - h + 1):
                for dw in range(W - w + 1):
                    weight = q[dh, dw, k]
                    if weight > 1e-10:
                        # Calculate squared error for background
                        diff_B = X[:, :, k] - B
                        s_squared += weight * np.sum(diff_B ** 2)
                        
                        # Correct for face region
                        diff_F_as_B = X[dh:dh+h, dw:dw+w, k] - B[dh:dh+h, dw:dw+w]
                        diff_F = X[dh:dh+h, dw:dw+w, k] - F
                        s_squared -= weight * np.sum(diff_F_as_B ** 2)
                        s_squared += weight * np.sum(diff_F ** 2)
                        
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
    import numpy as np
    
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
    import numpy as np
    
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
