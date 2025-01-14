
__version__ = "0.3.3"
__common_alias__ = "nppas"

from napari.types import SurfaceData, PointsData
from napari.types import LabelsData, ImageData

from napari_plugin_engine import napari_hook_implementation
from napari_tools_menu import register_function, register_action
import numpy as np
import napari

from ._surface_annotation_widget import SurfaceAnnotationWidget

from napari_time_slicer import time_slicer
from ._quantification import add_quality, Quality, add_curvature_scalars,\
    Curvature, add_spherefitted_curvature, surface_quality_table, \
    surface_quality_to_properties

@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return SurfaceAnnotationWidget

@napari_hook_implementation
def napari_experimental_provide_function():
    return [convex_hull,
            filter_smooth_simple,
            filter_smooth_laplacian,
            filter_smooth_taubin,
            simplify_vertex_clustering,
            simplify_quadric_decimation,
            subdivide_loop,
            labels_to_centroids,
            sample_points_uniformly,
            sample_points_poisson_disk,
            voxel_down_sample,
            points_to_labels,
            points_to_convex_hull_surface,
            surface_from_point_cloud_alpha_shape,
            surface_from_point_cloud_ball_pivoting,
            label_to_surface,
            largest_label_to_surface,
            add_quality,
            add_curvature_scalars,
            add_spherefitted_curvature]

def _knot_mesh() -> SurfaceData:
    import open3d
    from pathlib import Path
    data = str(Path(__file__).parent / "data" / "knot.ply")
    return isotropic_scale_surface(to_surface(open3d.io.read_triangle_mesh(data)), 0.1)

def _standford_bunny() -> SurfaceData:
    import open3d
    from pathlib import Path
    data = str(Path(__file__).parent / "data" / "bun_zipper.ply")
    return isotropic_scale_surface(to_surface(open3d.io.read_triangle_mesh(data)), 100)

def _vedo_ellipsoid() -> SurfaceData:
    import vedo
    shape = vedo.shapes.Ellipsoid()
    return isotropic_scale_surface((shape.points(), np.asarray(shape.faces())), 10)

@register_action(menu = "Surfaces > Example data: Knot (open3d, nppas)")
def example_data_knot(viewer:napari.viewer):
    viewer.add_surface(_knot_mesh(), blending='additive', shading='smooth')

@register_action(menu = "Surfaces > Example data: Standford bunny (nppas)")
def example_data_standford_bunny(viewer:napari.viewer):
    viewer.add_surface(_standford_bunny(), blending='additive', shading='smooth')

@register_action(menu = "Surfaces > Example data: Ellipsoid (vedo, nppas)")
def example_data_vedo_ellipsoid(viewer:napari.viewer):
    viewer.add_surface(_vedo_ellipsoid(), blending='additive', shading='smooth')

# todo: this doesn't work with surfaces:
#@napari_hook_implementation
#def napari_provide_sample_data():
#    return {
#        "KnotMesh": _knot_mesh,
#    }

def to_vector_d(data):
    import open3d
    return open3d.utility.Vector3dVector(data)


def to_vector_i(data):
    import open3d
    return open3d.utility.Vector3iVector(data)


def to_vector_double(data):
    import open3d
    return open3d.utility.DoubleVector(data)


def to_numpy(data):
    return np.asarray(data)


def to_mesh(data):
    import open3d
    return open3d.geometry.TriangleMesh(to_vector_d(data[0]), to_vector_i(data[1]))


def to_point_cloud(data):
    """
    http://www.open3d.org/docs/0.9.0/tutorial/Basic/working_with_numpy.html#from-numpy-to-open3d-pointcloud
    """
    import open3d
    pcd = open3d.geometry.PointCloud()
    pcd.points = to_vector_d(data)
    return pcd


def to_surface(mesh):
    vertices = to_numpy(mesh.vertices)
    faces = to_numpy(mesh.triangles)
    values = np.ones((vertices.shape[0]))

    return (vertices, faces, values)


@register_function(menu="Surfaces > Convex hull (open3d, nppas)")
def convex_hull(surface:SurfaceData) -> SurfaceData:
    """Produce the convex hull surface around a surface
    """
    mesh = to_mesh(surface)

    new_mesh, _ = mesh.compute_convex_hull()
    return to_surface(new_mesh)


@register_function(menu="Surfaces > Smoothing (simple, open3d, nppas)")
def filter_smooth_simple(surface:SurfaceData, number_of_iterations: int = 1) -> SurfaceData:
    """Smooth a surface using an average filter

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_iterations:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Average-filter
    """
    mesh_in = to_mesh(surface)
    mesh_out = mesh_in.filter_smooth_simple(number_of_iterations=number_of_iterations)
    return to_surface(mesh_out)


@register_function(menu="Surfaces > Smoothing (Laplacian, open3d, nppas)")
def filter_smooth_laplacian(surface:SurfaceData, number_of_iterations: int = 1) -> SurfaceData:
    """Smooth a surface using the Laplacian method

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_iterations:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Laplacian
    """
    mesh_in = to_mesh(surface)
    mesh_out = mesh_in.filter_smooth_laplacian(number_of_iterations=number_of_iterations)
    return to_surface(mesh_out)


@register_function(menu="Surfaces > Smoothing (Taubin et al 1995., open3d, nppas)")
def filter_smooth_taubin(surface:SurfaceData, number_of_iterations: int = 1) -> SurfaceData:
    """Smooth a surface using Taubin's method

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_iterations:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Taubin-filter
    ..[1] G. Taubin: Curve and surface smoothing without shrinkage, ICCV, 1995.
    """
    mesh_in = to_mesh(surface)
    mesh_out = mesh_in.filter_smooth_taubin(number_of_iterations=number_of_iterations)
    return to_surface(mesh_out)


@register_function(menu="Surfaces > Simplify using vertex clustering (open3d, nppas)")
def simplify_vertex_clustering(surface:SurfaceData, voxel_size: float = 5) -> SurfaceData:
    """Simplify a surface using vertex clustering

    Parameters
    ----------
    surface:napari.types.SurfaceData
    voxel_size:float

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Vertex-clustering
    """
    import open3d
    mesh_in = to_mesh(surface)

    mesh_out = mesh_in.simplify_vertex_clustering(
        voxel_size=voxel_size,
        contraction=open3d.geometry.SimplificationContraction.Average
    )
    return to_surface(mesh_out)


@register_function(menu="Surfaces > Simplify using quadratic decimation (open3d, nppas)")
def simplify_quadric_decimation(surface:SurfaceData, target_number_of_triangles: int = 500) -> SurfaceData:
    """Simplify a surface using quadratic decimation

    Parameters
    ----------
    surface:napari.types.SurfaceData
    target_number_of_triangles:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Mesh-decimation
    """
    mesh_in = to_mesh(surface)
    mesh_out = mesh_in.simplify_quadric_decimation(target_number_of_triangles=target_number_of_triangles)
    return to_surface(mesh_out)


@register_function(menu="Surfaces > Subdivide loop (open3d, nppas)")
def subdivide_loop(surface:SurfaceData, number_of_iterations: int = 1) -> SurfaceData:
    """Make a mesh more detailed by subdividing in a loop.
    If iterations are high, this can take very long.

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_iterations:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Mesh-subdivision
    """
    mesh_in = to_mesh(surface)
    mesh_out = mesh_in.subdivide_loop(number_of_iterations=number_of_iterations)
    return to_surface(mesh_out)


@register_function(menu="Points > Create points from labels centroids (nppas)")
def labels_to_centroids(labels_data:LabelsData, viewer:napari.Viewer = None) -> PointsData:
    """Determine centroids from all labels and store them as points.

    Parameters
    ----------
    labels_data:napari.types.LabelsData
    """
    from skimage.measure import regionprops

    statistics = regionprops(labels_data)
    centroids = [s.centroid for s in statistics]
    return centroids


@register_function(menu="Points > Create points from surface sampling uniformly (open3d, nppas)")
def sample_points_uniformly(surface:SurfaceData, number_of_points: int = 500, viewer:napari.Viewer=None) -> PointsData:
    """Sample points uniformly

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_points:int

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Sampling
    """
    mesh_in = to_mesh(surface)
    point_cloud = mesh_in.sample_points_uniformly(number_of_points=number_of_points)

    result = to_numpy(point_cloud.points)
    return result


@register_function(menu="Points > Create points from surface using Poisson disk sampling (open3d, nppas)")
def sample_points_poisson_disk(surface:SurfaceData, number_of_points: int = 500, init_factor: float = 5, viewer:napari.Viewer=None) -> PointsData:
    """Sample a list of points from a surface using the Poisson disk algorithm

    Parameters
    ----------
    surface:napari.types.SurfaceData
    number_of_points:int
    init_factor:float

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/mesh.html#Sampling
    """
    mesh_in = to_mesh(surface)
    point_cloud = mesh_in.sample_points_poisson_disk(number_of_points=number_of_points, init_factor=init_factor)

    result = to_numpy(point_cloud.points)
    return result


@register_function(menu="Points > Down-sample (open3d, nppas)")
def voxel_down_sample(points_data:PointsData, voxel_size: float = 5, viewer:napari.Viewer=None) -> PointsData:
    """Removes points from a point cloud so that the remaining points lie within a grid of
    defined voxel size.

    http://www.open3d.org/docs/0.12.0/tutorial/geometry/pointcloud.html#Voxel-downsampling
    """

    point_cloud = to_point_cloud(points_data)
    new_point_cloud = point_cloud.voxel_down_sample(voxel_size)

    result = to_numpy(new_point_cloud.points)
    return result


@register_function(menu="Points > Points to labels (nppas)")
@register_function(menu="Segmentation / labeling > Create labels from points (nppas)")
@time_slicer
def points_to_labels(points_data:PointsData, as_large_as_image:ImageData, viewer:napari.Viewer=None) -> LabelsData:
    """Mark single pixels in a zero-value pixel image if there is a point in a given point list.
    Point with index 0 in the list will get pixel intensity 1.
    If there are multiple points where the rounded coordinate is within the same pixel,
    some will be overwritten. There is no constraint which will be overwritten.

    Parameters
    ----------
    points_data:napari.types.PointsData
    as_large_as_image:napari.types.ImageData
        An image to specify the size of the output image. This image will not be overwritten.
    """

    labels_stack = np.zeros(as_large_as_image.shape, dtype=int)
    for i, p in enumerate(points_data):
        if len(labels_stack.shape) == 3:
            labels_stack[int(p[0] + 0.5), int(p[1] + 0.5), int(p[2] + 0.5)] = i + 1
        elif len(labels_stack.shape) == 2:
            labels_stack[int(p[0] + 0.5), int(p[1] + 0.5)] = i + 1
        else:
            raise NotImplementedError("Points to labels only supports 2D and 3D data")
            break

    return labels_stack

@register_function(menu="Surfaces > Surface to binary volumne (nppas)")
@register_function(menu="Segmentation / binarization > Create binary volume from surface (nppas)")
@time_slicer
def surface_to_binary_volume(surface: SurfaceData, as_large_as_image: ImageData,
                     viewer: napari.Viewer = None) -> LabelsData:
    """Render a closed surface as binary image with the same size as a specified image.

    Notes
    -----
    * The outlines of the binary volume are subject to numeric rounding issues and may not be voxel-perfect.

    See Also
    --------
    * [1] https://vedo.embl.es/autodocs/content/vedo/mesh.html#vedo.mesh.Mesh.binarize
    * [2] https://vedo.embl.es/autodocs/content/vedo/volume.html#vedo.volume.BaseVolume.tonumpy

    Parameters
    ----------
    surface: SurfaceData
    as_large_as_image: ImageData
    viewer: napari.Viewer, optional

    Returns
    -------
    binary_image:ImageData
    """
    import vedo

    my_mesh = vedo.mesh.Mesh((surface[0], surface[1]))
    vertices = my_mesh.points()  # get coordinates of surface vertices

    # get bounding box of mesh
    boundaries_l = np.min(vertices, axis=0).astype(int)
    boundaries_r = np.max(vertices, axis=0).astype(int)

    # replace region within bounding box with binary image
    binary_image = np.zeros_like(as_large_as_image)
    binary_image[boundaries_l[0] : boundaries_r[0],
                boundaries_l[1] : boundaries_r[1],
                boundaries_l[2] : boundaries_r[2]] = my_mesh.binarize().tonumpy()

    return binary_image


@register_function(menu="Surfaces > Convex hull of points (open3d, nppas)")
def points_to_convex_hull_surface(points_data:PointsData) -> SurfaceData:
    """Determine the convex hull surface of a list of points

    Parameters
    ----------
    points_data:napari.types.PointsData

    See Also
    --------
    ..[0] http://www.open3d.org/docs/0.12.0/tutorial/geometry/pointcloud.html#Convex-hull
    """

    point_cloud = to_point_cloud(points_data)
    mesh_out, _ = point_cloud.compute_convex_hull()

    return to_surface(mesh_out)


@register_function(menu="Surfaces > Create surface from points (alpha-shape, open3d, nppas)")
def surface_from_point_cloud_alpha_shape(points_data:PointsData, alpha:float = 5) -> SurfaceData:
    """Turn point into a surface using alpha shapes

    Parameters
    ----------
    points_data:napari.types.PointsData
    alpha:float

    See Also
    --------
    ..[0] http://www.open3d.org/docs/latest/tutorial/Advanced/surface_reconstruction.html#Alpha-shapes
    """
    import open3d
    pcd = to_point_cloud(points_data)
    mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    return to_surface(mesh)


@register_function(menu="Surfaces > Create surface from points (ball-pivoting, open3d, nppas)")
def surface_from_point_cloud_ball_pivoting(points_data:PointsData, radius: float = 5, delta_radius=0) -> SurfaceData:
    """Turn point into a surface using ball pivoting

    Parameters
    ----------
    points_data:napari.types.PointsData
    radius:float
        ball radius
    delta_radius:float, optional
        if specified, radii = [radius - delta_radius, radius, radius + delta_radius] will
        be used as ball radii

    See Also
    --------
    ..[0] http://www.open3d.org/docs/latest/tutorial/Advanced/surface_reconstruction.html#Ball-pivoting
    ..[1] http://www.open3d.org/docs/0.7.0/tutorial/Basic/pointcloud.html#point-cloud
    """
    import open3d
    pcd = to_point_cloud(points_data)

    pcd.estimate_normals(search_param=open3d.geometry.KDTreeSearchParamHybrid(radius=0.1,
                                                                              max_nn=30))
    if delta_radius == 0:
        radii = [radius]
    else:
        radii = [radius - delta_radius, radius, radius + delta_radius]

    mesh = open3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, to_vector_double(radii))
    return to_surface(mesh)


@register_function(menu="Surfaces > Create surface from any label (marching cubes, scikit-image, nppas)")
@time_slicer
def label_to_surface(labels: LabelsData, label_id: int = 1) -> SurfaceData:
    """
    Turn a single label out of a label image into a surface using the marching cubes algorithm

    Parameters
    ----------
    labels_data:napari.types.LabelsData
    label_id: int
    """
    from skimage.measure import marching_cubes

    binary = np.asarray(labels == label_id)

    vertices, faces, normals, values = marching_cubes(binary, 0)

    return (vertices, faces, values)


@register_function(menu="Surfaces > Create surface from largest label (marching cubes, scikit-image, nppas)")
@time_slicer
def largest_label_to_surface(labels: LabelsData) -> SurfaceData:
    """
    Turn the largest label in a label image into a surface using the marching cubes algorithm

    Parameters
    ----------
    labels_data:napari.types.LabelsData
    """
    from skimage.measure import regionprops
    statistics = regionprops(labels)

    label_index = np.argmax([r.area for r in statistics])
    labels_list = [r.label for r in statistics]
    label = labels_list[label_index]

    return label_to_surface(labels, label)

@register_function(menu="Surfaces > Fill holes (vedo, nppas)")
def fill_holes(surface: SurfaceData, size_limit: float = 100) -> SurfaceData:
    """
    Fill holes in a surface up to a specified size.

    Parameters
    ----------
    surface : napari.layers.Surface
    size_limit : float, optional
        Size limit to hole-filling. The default is 100.

    See also
    --------
    ..[0] https://vedo.embl.es/autodocs/content/vedo/mesh.html#vedo.mesh.Mesh.fillHoles
    """
    import vedo

    mesh = vedo.mesh.Mesh((surface[0], surface[1]))
    mesh.fillHoles(size=size_limit)

    return (mesh.points(), np.asarray(mesh.faces()))

@register_function(menu = "Surfaces > Scale surface (isotropic, nppas)",
                   scale_factor={'min':0.01, 'max':100000})
def isotropic_scale_surface(surface:SurfaceData, scale_factor:float = 1) -> SurfaceData:
    """
    Scales a surface with a given factor.

    Parameters
    ----------
    surface
    scale_factor

    Returns
    -------
    surface
    """
    result = list(surface)
    result[0] = result[0] * scale_factor
    return tuple(result)

