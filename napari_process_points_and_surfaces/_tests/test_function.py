# from napari_segment_blobs_and_things_with_membranes import threshold, image_arithmetic

# add your tests here...


def test_something():
    from napari_process_points_and_surfaces import convex_hull,\
            filter_smooth_simple,\
            filter_smooth_laplacian,\
            filter_smooth_taubin,\
            simplify_vertex_clustering,\
            simplify_quadric_decimation,\
            subdivide_loop,\
            labels_to_centroids,\
            sample_points_uniformly,\
            sample_points_poisson_disk,\
            voxel_down_sample,\
            points_to_labels,\
            points_to_convex_hull_surface,\
            surface_from_point_cloud_alpha_shape,\
            surface_from_point_cloud_ball_pivoting,\
            label_to_surface,\
            largest_label_to_surface,\
            add_quality,\
            Quality,\
            fill_holes

    from skimage.data import cells3d
    nuclei = cells3d()[:, 1, 60:120, 30:80]

    from skimage.measure import label
    labels = label(nuclei > 20000)

    surface = label_to_surface(labels, 3)

    surface = largest_label_to_surface(labels)

    convex_hull(surface)
    filter_smooth_simple(surface)
    filter_smooth_taubin(surface)
    filter_smooth_laplacian(surface)
    simplify_quadric_decimation(surface)
    simplify_vertex_clustering(surface)
    subdivide_loop(surface)
    labels_to_centroids(labels)
    sample_points_uniformly(surface)
    points = sample_points_poisson_disk(surface)
    voxel_down_sample(points)
    points_to_labels(points, labels)
    surface = points_to_convex_hull_surface(points)
    surface = fill_holes(surface)
    surface_from_point_cloud_ball_pivoting(points)
    surface_from_point_cloud_alpha_shape(points)
    add_quality(surface, Quality.SKEW)

def test_curvature():
    from napari_process_points_and_surfaces import add_curvature_scalars,\
        Curvature,\
        add_spherefitted_curvature
    import vedo
    import numpy as np

    shape = vedo.shapes.Ellipsoid()
    surface_data = (shape.points(), np.asarray(shape.faces()))

    add_curvature_scalars(surface_data, Curvature.Gauss_Curvature)
    add_curvature_scalars(surface_data, Curvature.Mean_Curvature)
    add_curvature_scalars(surface_data, Curvature.Maximum_Curvature)
    add_curvature_scalars(surface_data, Curvature.Minimum_Curvature)

    add_spherefitted_curvature(surface_data, radius=1)

def test_surface_to_binary_volume():
    import numpy as np
    from napari_process_points_and_surfaces import largest_label_to_surface, surface_to_binary_volume
    image = np.zeros((32, 32, 32)).astype(int)
    image[1:30, 1:30, 1:30] = 1

    surface = largest_label_to_surface(image)
    binary_image = surface_to_binary_volume(surface, image)

    overlap = np.logical_and(image, binary_image)
    union = np.logical_or(image, binary_image)

    jaccard_index = np.sum(overlap) / np.sum(union)

    assert jaccard_index > 0.9

def test_surface_to_measurement_table():
    import numpy as np
    from napari_process_points_and_surfaces import largest_label_to_surface, surface_quality_table, Quality
    image = np.zeros((32, 32, 32)).astype(int)
    image[1:30, 1:30, 1:30] = 1

    surface = largest_label_to_surface(image)
    table = surface_quality_table(surface, qualities=[Quality.MIN_ANGLE, Quality.MAX_ANGLE, Quality.AREA])
    assert len(table.keys()) == 4

