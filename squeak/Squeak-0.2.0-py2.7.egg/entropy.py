import pandas as pd

rx =  pd.read_csv('data/rx.csv')
ry =  pd.read_csv('data/ry.csv')

x = rx.iloc[0]
y = ry.iloc[0]

# Or 

nx =  pd.read_csv('data/nx.csv')
ny =  pd.read_csv('data/ny.csv')

x = nx.iloc[0]
y = ny.iloc[0]

dx = x.diff()

'''
R code for function pracma::sample_entropy

function (ts, edim = 2, r = 0.2 * sd(ts), tau = 1) 
{
    stopifnot(is.numeric(ts), is.numeric(edim))
    if (tau > 1) {
        s <- seq(1, length(ts), by = tau)
        ts <- ts[s]
    }
    N <- length(ts)
    correl <- numeric(2)
    datamat <- zeros(edim + 1, N - edim)
    for (i in 1:(edim + 1)) datamat[i, ] <- ts[i:(N - edim + 
        i - 1)]
    for (m in edim:(edim + 1)) {
        count <- zeros(1, N - edim)
        tempmat <- datamat[1:m, ]
        for (i in 1:(N - m - 1)) {
            X <- abs(tempmat[, (i + 1):(N - edim)] - repmat(tempmat[, 
                i, drop = FALSE], 1, N - edim - i))
            dst <- apply(X, 2, max)
            d <- (dst < r)
            count[i] <- sum(d)/(N - edim)
        }
        correl[m - edim + 1] <- sum(count)/(N - edim)
    }
    return(log(correl[1]/correl[2]))
}
'''

def sample_entropy(ts, edim = 2, r = .2 * np.std(ts), tau = 1):
    N = len(ts)
    # edim is the window size, so we're going to make a matrix of
    # contiguous values at the larger (edim+1) window size.
    correl = []
    datamat = np.zeros((edim+1, N-edim-1)) # 3x98
    for i in range(1, (edim+1)+1): # 1 to the larger window size
        datamat[i-1] =  ts[i-1:N-edim+i-2] #ts[i-1:N-edim+i+1]
    for m in [edim, edim+1]:
        # For window size edim, and edim+1
        count = np.zeros((1, N-edim-1))
        tempmat = datamat[:m,] # Windows of current size
        for i in range(N-m-1): # For every window...
            a = tempmat[..., i:N-edim-1]
            b = np.transpose([tempmat[..., i-1]]*(N-edim-i-1))
            X = np.abs(a-b)
            dst = np.max(X, axis=0)
            d = dst < r
            count[...,i] = float(sum(d)) / (N - edim)
        correl.append( sum(count) / (N - edim) )
    return np.log(correl[0] / correl[1])

"""
> pracma::approx_entropy
function (ts, edim = 2, r = 0.2 * sd(ts), elag = 1) 
{
    N <- length(ts)
    result <- numeric(2)
    for (j in 1:2) {
        m <- edim + j - 1
        phi <- zeros(1, N - m + 1)
        dataMat <- zeros(m, N - m + 1)
        for (i in 1:m) dataMat[i, ] <- ts[i:(N - m + i)]
        for (i in 1:(N - m + 1)) {
            tempMat <- abs(dataMat - repmat(dataMat[, i, drop = FALSE], 
                1, N - m + 1))
            boolMat <- apply(tempMat > r, 2, max)
            phi[i] <- sum(!boolMat)/(N - m + 1)
        }
        result[j] <- sum(phi)/(N - m + 1)
    }
    apen <- log(result[1]/result[2])
    return(apen)
}
"""

def approx_entropy(ts, edim = 2, r = 0.2 * sd(ts), elag = 1):
    N = len(ts)
    result = []
    for j in [1, 2]:
        m = edim + j - 1
        phi = []
        dataMat = np.zeros((m, N-m+1))
        for i in range(m):
            dataMat[i,] = ts[i:(N-m+i+1)]
        for i in range(N-m+1):
            rep = np.transpose([dataMat[..., i-1]]*(N-m+1))
            tempMat = np.abs(dataMat - rep)
            boolMat = np.max(tmpMat > r, axis=0)
            phi.append( float(np.sum(~boolMat)) / (N-m+1) )


