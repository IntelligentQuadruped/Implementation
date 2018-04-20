'''
Author: Viveque Ramji

'''

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon    
from matplotlib.path import Path
from colorized_voronoi import voronoi_finite_polygons_2d


def get_voronoi(shape, samples, vec):
    h,w = shape
    mask = np.where(vec != 0)
    samples = samples[mask]
    vec = vec[mask]

    he = np.arange(0, h)
    wi = np.arange(0, w)

    Yq, Zq = np.meshgrid(wi, he)
    Y_sample = Yq.flatten()[samples]
    Z_sample = Zq.flatten()[samples]

    points = np.column_stack((Y_sample, Z_sample))
    voronoi = Voronoi(points)

    regions, vertices = voronoi_finite_polygons_2d(voronoi)
    reconstructed = np.zeros((w, h))
    b = Polygon([(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)])

    reconstructed = np.zeros((w, h))

    for i, region in enumerate(regions):
        polygon = vertices[region]
        shape = Polygon(polygon)
        if not b.contains(shape):
            shape = shape.intersection(b)

        x, y = shape.exterior.coords.xy

        row_indices = np.array(x, dtype=np.int16)
        column_indices = np.array(y, dtype=np.int16)

        row_min = np.amin(row_indices)
        row_max = np.amax(row_indices) + 1
        column_min = np.amin(column_indices)
        column_max = np.amax(column_indices) + 1

        enclose = np.zeros((row_max-row_min, column_max-column_min))
        enclose_rows = row_indices-row_min
        enclose_columns = column_indices-column_min

        enclose[enclose_rows, enclose_columns] = 1 

        points = np.indices(enclose.shape).reshape(2, -1).T
        path = Path(zip(x-row_min,y-column_min))

        mask = path.contains_points(points, radius=-1e-9)
        mask = mask.reshape(enclose.shape)

        reconstructed_rows, reconstructed_columns = np.where(mask)

        reconstructed[row_min+reconstructed_rows, column_min+reconstructed_columns] = vec[i]

    return reconstructed.T


if __name__ == "__main__":
    """
    Application example with visualization.
    """
    import matplotlib.pyplot as plt
    import sparse_interpolation as si

    # depth = np.array([[1, np.nan, 2, np.nan, 1, 1.2, np.nan, np.nan, 4], 
    #                   [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 3, np.nan],
    #                   [np.nan, np.nan, 1, np.nan, np.nan, 1, np.nan, np.nan, np.nan],
    #                   [.2, np.nan, np.nan, np.nan, 1, np.nan, 1, 4, np.nan]])
    depth = 5*np.random.rand(10, 10)
    # depth = np.vstack((depth, depth, depth, depth))


    samples, measured = si.createSamples(depth, .2)
    print(samples.shape)

    dep_comp = get_voronoi(depth.shape, samples, measured)

    plt.subplot(2, 1, 1)
    plt.imshow(depth)
    plt.subplot(2, 1, 2)
    plt.imshow(dep_comp)
    plt.show()





