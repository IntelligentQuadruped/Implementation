"""
Author:         Jan Bernhard
Purpose:        Filling in data gaps in the R200 depth sensor output.
Performance:    Number of calculations increase as set standard-deviation (SIGMA)
                parameter decreases. A sigma of 450 allows a depth inaccuracy of 45cm 
"""

import numpy as np

def setSigma(matrix, num=2):
    """
    Sets starting sigma value by interpolating from emperically
    determined data from R200 camera. 

    Default is a 3 sigma to get 95% of the values. 
    """
    x = matrix[matrix > 0].mean()
    a,b = [0.07064656, -0.03890366]
    sigma = a*x + b
    return num*round(sigma, 3)


def split(matrix):
    """
    Splits matrix into 4 equally sized rectangles.

    Arg:
        matrix - numpy 2D depth matrix
    Returns:
        4 matrix quarters as list
    """
    h,w = matrix.shape
    h_prime = int(h/2)
    w_prime = int(w/3)

    # quarter matrices
    upper_left = matrix[:h_prime,:w_prime]
    upper_middle = matrix[:h_prime,w_prime:2*w_prime]
    upper_right = matrix[:h_prime,2*w_prime:w]
    lower_left = matrix[h_prime:,:w_prime]
    lower_middle = matrix[h_prime:,w_prime:2*w_prime]
    lower_right = matrix[h_prime:,2*w_prime:w]

    return [upper_left,upper_middle,upper_right,lower_left,lower_middle,lower_right]


def average(matrix, sigma, min_h):
    """
    Assigns mean of all non-zero values to each gridcell given that the 
    standard deviations is within bounds and the quarters don't split below the 
    minimum grid cell size. Inaccuracy is likely around 10%, sigma of up to 500, 
    when images include multiple objects of different depths close together.

    Args:
        matrix - numpy 2D depth matrix
        sigma - Threshold value for standard deviation.
    Returns:
        matrix - 2d depth matrix with approximated values.
    """
    h,w = matrix.shape
    if matrix[matrix > 0].std() > sigma and h >= min_h:
        submatrices = split(matrix)
        for i, submatrix in enumerate(submatrices):
            submatrices[i] = average(submatrix,sigma, min_h)
        
        horizontal1 = np.hstack((submatrices[0],submatrices[1],submatrices[2]))
        horizontal2 = np.hstack((submatrices[3],submatrices[4],submatrices[5]))
        stacked = np.vstack((horizontal1,horizontal2))
        return stacked

    else:
        ave_depth_value = matrix[matrix > 0].mean()
        matrix = np.full((h,w), ave_depth_value)
        return matrix

def cleanup(matrix, n):
    """
    In case some grid cells are left with a 0.0 as mean-value. It assigns the value 
    to the grid cell of the next non-zero gridcell. 
    """
    x,y = np.where(np.isnan(matrix))
    h,w = matrix.shape
    for xc,yc in zip(x,y):
        higher = [xc,yc]
        lower = [xc,yc]
        while(True):
            if higher[1] + n < w:
                higher[1] = higher[1] + n
            if lower[1] - n > 0:
                lower[1] = lower[1] - n
            if (not np.isnan(matrix[xc, higher[1]])) or (not np.isnan(matrix[xc, lower[1]])):
                matrix[xc,yc] = matrix[xc, higher[1]] if not np.isnan(matrix[xc, higher[1]]) else matrix[lower[0], lower[1]]
                break
    return matrix

def depthCompletion(d, min_sigma, min_h):
    """
    Manages the appropriate sequence of completion steps to determine a depth 
    estimate for each matrix entry. 
    Args:
        matrix - depth values as np.array()
        min_sigma - acceptable deviation within calculated depth fields
    """

    # Reduces outliers to a maximum value of 4.0 which is the max
    # sensitivity value of the R200 depth sensors.

    depth = d.copy()
    # std = setSigma(matrix)
    # min_sigma = std if min_sigma < std else min_sigma

    avg = average(depth, min_sigma, min_h)
    clean = cleanup(avg, min_h/2)
    return clean


if __name__ == "__main__":
    """
    Application example with visualization.
    """
    import matplotlib.pyplot as plt

    depth = 4*np.random.rand(4, 10)
    depth[0, 5] = np.nan
    depth[0, 6] = np.nan
    depth[depth>4.0] = 0.0

    dep_comp = depthCompletion(depth, .001, 2)

    plt.subplot(2, 1, 1)
    plt.imshow(depth)
    plt.subplot(2, 1, 2)
    plt.imshow(dep_comp)
    plt.show()
else:
    np.warnings.filterwarnings('ignore')




