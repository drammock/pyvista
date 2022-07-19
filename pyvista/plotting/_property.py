"""This module contains the Property class."""
from functools import lru_cache

import pyvista
from pyvista import _vtk

from .colors import Color


@lru_cache(maxsize=None)
def _check_supports_pbr():
    """Check if VTK supports physically based rendering."""
    if not _vtk.VTK9:  # pragma: no cover
        from pyvista.core.errors import VTKVersionError

        raise VTKVersionError('Physically based rendering requires VTK 9 or newer.')


class Property(_vtk.vtkProperty):
    """Wrap vtkProperty."""

    def __init__(
        self,
        theme=None,
        interpolation=None,
        color=None,
        style=None,
        metallic=None,
        roughness=None,
        point_size=None,
        opacity=None,
        ambient=None,
        diffuse=None,
        specular=None,
        specular_power=None,
        show_edges=None,
        edge_color=None,
        render_points_as_spheres=None,
        render_lines_as_tubes=None,
        lighting=None,
        line_width=None,
        culling=None,
    ):
        """Initialize this property."""
        self._theme = pyvista.themes.DefaultTheme()
        if theme is None:
            # copy global theme to ensure local property theme is fixed
            # after creation.
            self._theme.load_theme(pyvista.global_theme)
        else:
            if not isinstance(theme, pyvista.themes.DefaultTheme):
                raise TypeError(
                    'Expected ``pyvista.themes.DefaultTheme`` for '
                    f'``theme``, not {type(theme).__name__}.'
                )
            self._theme.load_theme(theme)

        self.interpolation = interpolation
        self.color = color
        self.style = style
        if interpolation == 'Physically based rendering':
            if metallic is not None:
                self.metallic = metallic
            if roughness is not None:
                self.roughness = roughness
        self.point_size = point_size
        if opacity is not None:
            self.opacity = opacity
        if ambient is not None:
            self.ambient = ambient
        if diffuse is not None:
            self.diffuse = diffuse
        if specular is not None:
            self.specular = specular
        if specular_power is not None:
            self.specular_power = specular_power
        self.show_edges = show_edges
        self.edge_color = edge_color
        self.render_points_as_spheres = render_points_as_spheres
        self.render_lines_as_tubes = render_lines_as_tubes
        self.lighting = lighting
        self.line_width = line_width

        if culling is not None:
            self.culling = culling

    @property
    def style(self) -> str:
        """Return or set the representation."""
        return self.GetRepresentationAsString()

    @style.setter
    def style(self, new_style: str):
        if new_style is None:
            new_style = 'surface'
        new_style = new_style.lower()

        if new_style == 'wireframe':
            self.SetRepresentationToWireframe()
            if not self._color_set:
                self.color = self._theme.outline_color
        elif new_style == 'points':
            self.SetRepresentationToPoints()
        elif new_style == 'surface':
            self.SetRepresentationToSurface()
        else:
            raise ValueError(
                f'Invalid style "{new_style}".  Must be one of the following:\n'
                '\t"surface"\n'
                '\t"wireframe"\n'
                '\t"points"\n'
            )

    @property
    def color(self):
        """Return or set the color of this property."""
        return Color(self.GetColor())

    @color.setter
    def color(self, new_color):
        self._color_set = new_color is None
        rgb_color = Color(new_color, default_color=self._theme.color)
        self.SetColor(rgb_color.float_rgb)

    @property
    def edge_color(self):
        """Return or set the edge color of this property."""
        return Color(self.GetEdgeColor())

    @edge_color.setter
    def edge_color(self, new_color):
        rgb_color = Color(new_color, default_color=self._theme.edge_color)
        self.SetEdgeColor(rgb_color.float_rgb)

    @property
    def opacity(self):
        """Return or set the opacity of this property."""
        return self.GetOpacity()

    @opacity.setter
    def opacity(self, value):
        if value is None:
            return
        self.SetOpacity(value)

    @property
    def show_edges(self):
        """Return or set show edges."""
        return self.GetEdgeVisibility()

    @show_edges.setter
    def show_edges(self, value):
        if value is None:
            value = self._theme.show_edges
        self.SetEdgeVisibility(value)

    @property
    def lighting(self) -> bool:
        """Return or set lighting."""
        return self.SetLighting()

    @lighting.setter
    def lighting(self, value):
        if value is None:
            value = self._theme.lighting
        self.SetLighting(value)

    @property
    def ambient(self):
        """Return or set ambient."""
        return self.GetAmbient()

    @ambient.setter
    def ambient(self, new_ambient):
        self.SetAmbient(new_ambient)

    @property
    def diffuse(self):
        """Return or set diffuse."""
        return self.GetDiffuse()

    @diffuse.setter
    def diffuse(self, new_diffuse):
        self.SetDiffuse(new_diffuse)

    @property
    def specular(self):
        """Return or set specular."""
        return self.GetSpecular()

    @specular.setter
    def specular(self, new_specular):
        self.SetSpecular(new_specular)

    @property
    def specular_power(self):
        """Return or set specular power."""
        return self.GetSpecularPower()

    @specular_power.setter
    def specular_power(self, new_specular_power):
        self.SetSpecularPower(new_specular_power)

    @property
    def metallic(self):
        """Return or set metallic."""
        _check_supports_pbr()
        return self.GetMetallic()

    @metallic.setter
    def metallic(self, new_metallic):
        _check_supports_pbr()
        self.SetMetallic(new_metallic)

    @property
    def roughness(self):
        """Return or set roughness."""
        _check_supports_pbr()
        return self.GetRoughness()

    @roughness.setter
    def roughness(self, new_roughness):
        _check_supports_pbr()
        self.SetRoughness(new_roughness)

    @property
    def interpolation(self) -> str:
        """Return or set show edges of this property."""
        return self.GetInterpolationAsString()

    @interpolation.setter
    def interpolation(self, new_interpolation):
        if new_interpolation == 'Physically based rendering':
            _check_supports_pbr()

            self.SetInterpolationToPBR()
        elif new_interpolation == 'Phong':
            self.SetInterpolationToPhong()
        elif new_interpolation == 'Gouraud':
            self.SetInterpolationToGouraud()
        elif new_interpolation == 'Flat' or new_interpolation is None:
            self.SetInterpolationToFlat()
        else:
            raise ValueError(f'Invalid interpolation "{new_interpolation}"')

    @property
    def render_points_as_spheres(self):
        """Return or set rendering points as spheres."""
        self.GetRenderPointsAsSpheres()

    @render_points_as_spheres.setter
    def render_points_as_spheres(self, new_render_points_as_spheres):
        if new_render_points_as_spheres is None:
            return
        self.SetRenderPointsAsSpheres(new_render_points_as_spheres)

    @property
    def render_lines_as_tubes(self):
        """Return or set rendering lines as tubes."""
        self.GetRenderLinesAsTubes()

    @render_lines_as_tubes.setter
    def render_lines_as_tubes(self, new_value):
        if new_value is None:
            return
        self.SetRenderLinesAsTubes(new_value)

    @property
    def line_width(self):
        """Return or set the line width."""
        self.GetLineWidth()

    @line_width.setter
    def line_width(self, new_size):
        if new_size is None:
            return
        self.SetLineWidth(new_size)

    @property
    def point_size(self):
        """Return or set the point size."""
        self.GetPointSize()

    @point_size.setter
    def point_size(self, new_size):
        if new_size is None:
            return
        self.SetPointSize(new_size)

    @property
    def culling(self):
        """Return or set face culling."""
        if self.BackfaceCullingOn():
            return 'back'
        elif self.FrontfaceCullingOn():
            return 'front'
        return

    @culling.setter
    def culling(self, value):
        if isinstance(value, str):
            value = value.lower()

        if value in [True, 'back', 'backface', 'b']:
            try:
                self.BackfaceCullingOn()
            except AttributeError:  # pragma: no cover
                pass
        elif value in ['front', 'frontface', 'f']:
            try:
                self.FrontfaceCullingOn()
            except AttributeError:  # pragma: no cover
                pass
        else:
            raise ValueError(
                f'Culling option ({value}) not understood. Should be either:\n'
                'True, "back", "backface", "b", "front", "frontface", or "f"'
            )
