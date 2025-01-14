# napari-process-points-and-surfaces (nppas)

[![License](https://img.shields.io/pypi/l/napari-process-points-and-surfaces.svg?color=green)](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-process-points-and-surfaces.svg?color=green)](https://pypi.org/project/napari-process-points-and-surfaces)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-process-points-and-surfaces.svg?color=green)](https://python.org)
[![tests](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/workflows/tests/badge.svg)](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/actions)
[![codecov](https://codecov.io/gh/haesleinhuepf/napari-process-points-and-surfaces/branch/master/graph/badge.svg)](https://codecov.io/gh/haesleinhuepf/napari-process-points-and-surfaces)
[![Development Status](https://img.shields.io/pypi/status/napari-process-points-and-surfaces.svg)](https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-process-points-and-surfaces)](https://napari-hub.org/plugins/napari-process-points-and-surfaces)

Process and analyze surfaces using [open3d](http://www.open3d.org/) and [vedo](https://vedo.embl.es/) in [napari].

## Usage

You find a couple of surface generation, smoothing and analysis functions in the menu `Tools > Surfaces` and `Tools > Points`. For detailed explanation of the underlying algorithms, please refer to the [open3d](http://www.open3d.org/docs/release/) documentation.
Some code snippets and the knot example data have been taken from the open3d project which is 
[MIT licensed](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/blob/main/licenses_third_party/open3d_LICENSE) 
and from the [vedo documentation](https://vedo.embl.es/autodocs/index.html) 
which is [MIT licensed](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/blob/main/licenses_third_party/vedo_LICENSE).
The Standford Bunny example dataset has been taken from the [The Stanford 3D Scanning Repository](http://graphics.stanford.edu/data/3Dscanrep/).

For processing meshes in Python scripts, see the [demo notebook](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/blob/main/docs/demo.ipynb). There you also learn how this screenshot is made:

![img.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/screenshot.png)

For performing quantitative measurements of meshes in Python scripts, see the [demo notebook](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/blob/main/docs/quality_measurements.ipynb). 
There you also learn how this screenshot is made:

![img.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/screenshot2.png)

### Surface measurements and annotations

Using the menu `Tools > Measurement > Surface quality table (vedo, nppas)` you can derived quantiative measurements of
the vertices in a given surface layer. 

![img_1.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/surface_measurements.png)

To differentiate regions when analyzing those measurements it is recommended to use the menu `Tools > Surfaces > Annotate surface manually (nppas)`
after measurements have been made. This tool allows you to draw annotation label values on the surface. 
It is recommended to do activate a colorful colormap such as `hsv` before starting to draw annotations. 
Furthermore, set the maximum of the contrast limit range to the number of regions you want to annotate + 1.
Annotations can be drawn as freehand lines and circles.

![img.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/surface_annotation.png)

After measurements and annotations were done, you can save the annotation in the same measurement table using the menu
`Tools > Measurement > Surface quality/annotation to table (nppas)`

![img.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/surface_annotation_in_table.png)

### Measurement visualization

To visualize measurements on the surface, just double-click on the table column headers. This also allows to visualize 
measurements and annotations side-by-side.

![img.png](https://github.com/haesleinhuepf/napari-process-points-and-surfaces/raw/main/docs/measurement_visualization.gif)

## Installation

You can install `napari-process-points-and-surfaces` via [pip] and conda:

```
conda create -n nppas-env -c conda-forge -c open3d-admin python=3.9 open3d napari
conda activate nppas-env
pip install napari-process-points-and-surfaces
```

## See also

There are other napari plugins with similar / overlapping functionality
* [pymeshlab](https://www.napari-hub.org/plugins/napari-pymeshlab)
* [morphometrics](https://www.napari-hub.org/plugins/morphometrics)  
* [napari-pyclesperanto-assistant](https://www.napari-hub.org/plugins/napari-pyclesperanto-assistant)

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-process-points-and-surfaces" is free and open source software

## Issues

If you encounter any problems, please create a thread on [image.sc] along with a detailed description and tag [@haesleinhuepf].

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/haesleinhuepf/napari-process-points-and-surfaces/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

[image.sc]: https://image.sc
[@haesleinhuepf]: https://twitter.com/haesleinhuepf
