import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon    
from matplotlib.path import Path

def voronoi_finite_polygons_2d(vor, radius=None):
    """
    @misc{col_vo,
        title = {Colorized Voronoi diagram with Scipy, in 2D, including infinite regions},
        howpublished = "\url{https://gist.github.com/pv/8036995}",
        year = {2013}, 
        note = "[Online; accessed 16-April-2018]"
    }

    
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """

    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input")

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max()

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all(v >= 0 for v in vertices):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1] # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    return new_regions, np.asarray(new_vertices)


def get_voronoi(points):

    vor = Voronoi(points)

    regions, vertices = voronoi_finite_polygons_2d(vor)
    arr = np.zeros((w, h))
    b = Polygon([(0, 0), (w-1, 0), (w-1, h-1), (0, h-1)])

    arr = np.zeros((w, h))

    for i, region in enumerate(regions):
        polygon = vertices[region]
        shape = Polygon(polygon)
        if not b.contains(shape):
            shape = shape.intersection(b)

        x, y = shape.exterior.coords.xy

        row_indices = np.array(x, dtype=np.int16)
        col_indices = np.array(y, dtype=np.int16)

        rmin = np.amin(row_indices)
        rmax = np.amax(row_indices)+1

        cmin = np.amin(col_indices)
        cmax = np.amax(col_indices)+1

        tmp = np.zeros((rmax-rmin, cmax-cmin))
        tmpr = row_indices-rmin
        tmpc = col_indices-cmin

        tmp[tmpr, tmpc] = 1 

        points = np.indices(tmp.shape).reshape(2, -1).T
        path = Path(zip(x-rmin,y-cmin))

        mask = path.contains_points(points, radius=1e-9)
        mask = mask.reshape(tmp.shape)

        amr, amc = np.where(mask)

        arr[rmin+amr, cmin+amc] = vec[i]

    return arr.T
