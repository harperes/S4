# from ._S4 import S4_Simulation
__version__ = "1.1.5"
from ._S4 import S4_Simulation as _S4Sim
import numpy as np
import warnings
# from . import S4


class Simulation:
    """RCWA Simulation

    .. moduleauthor:: Eric Harper <eric.harper.1.ctr@us.af.mil>

    """
    def __init__(self):
        # "pointer" to the PyBind11 C++ Object
        self._S4Sim = _S4Sim()
        # boolean indicating if a simulation object is created
        # could thing about automatically creating a simulation...
        self._hasSim = False

    def _check_for_sim(self):
        """
        Helper function to check to make sure that a simulation object exists;
        otherwise, segmentation faults may occur
        """
        if not self._hasSim:
            raise RuntimeError("No simulation found. Aborting.")

    def _count_nans(self, arr):
        """
        Check for the number of nan values in a numpy array


        :param arr: array to check number of nan values in
        :type arr: :class:`numpy.ndarray`, dtype=float
        :return: number of nans in array
        :type: int
        """
        l_arr = np.asarray(arr)
        l_arr = np.require(l_arr, requirements=["C"])
        return int(np.count_nonzero(np.isnan(arr)))

    def _set_nan_to_zero(self, arr):
        """
        Set all nan values to 0


        :param arr: array to check number of nan values in
        :type arr: :class:`numpy.ndarray`, dtype=float
        """
        arr[np.isnan(arr)] = 0.0

    def _sanitize_array(self, arr, dtype=np.float64, warn_name=None):
        """
        sanitize a given array for input into S4 cpp function

        :param arr: array to sanitize
        :type arr: :class:`numpy.ndarray`
        :param dtype: type to set array to
        :type dtype: :class:`numpy.dtype`
        :return: sanitized array
        :type: :class:`numpy.ndarray`
        """
        arr = np.require(arr, dtype=dtype, requirements=["C"])
        # there is now a chance that nan values are in the array and will
        # result in uncaught improper calculations
        # count the number of nans
        n_nan = self._count_nans(arr)
        if n_nan != 0:
            warnings.warn(f"np.nan found in {warn_name}. These values will be \
                set to 0. Please check angles to ensure all values supplied.")
            self._set_nan_to_zero(arr)
        return arr

    def create_new(self):
        """
        Create a new simulation instance

        """
        self._S4Sim._CreateNew()
        self._hasSim = True

    def _material_array_check(self, eps):
        """
        Helper function to check values of the eps array

        :param eps: epsilon value of material
        :type eps: lorem ipsum

        :return: l_eps
        :type: lorem ipsum
        """

        l_eps = np.asarray(eps)
        if l_eps.ndim > 3:
            raise RuntimeError("eps must be a 1- or 2-Dimensional array")
        if l_eps.ndim == 1:
            ndims = [1, 2, 18]
            if not l_eps.shape[0] in ndims:
                err_str = ("the shape of eps must be a "
                           "1, 2, or 18 element array")
                raise RuntimeError(err_str)
        elif l_eps.ndim == 3:
            if not ((l_eps.shape[0] == 3) and
                    (l_eps.shape[1] == 3) and
                    (l_eps.shape[2] == 2)):
                raise RuntimeError("eps must be a 3x3x2 array")
        l_eps = self._sanitize_array(l_eps, dtype=np.float64, warn_name="eps")
        return l_eps

    def add_material(self, name, eps):
        """
        Add a material to the simulation

        :param name: name of the material
        :param eps: epsilon value of the material
        :type name: str
        :type eps: :class:`numpy.ndarray`, shape=(:math:`1` OR :math:`2` OR
                   :math:`9` OR :math:`3 \\times 3`), dtype=float
        """
        # check to make sure a simulation exists
        self._check_for_sim()

        # check types, raise errors as needed
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        l_eps = self._material_array_check(eps)
        # add the material as requested
        self._S4Sim._AddMaterial(l_name, l_eps)

    def set_material(self, name, eps):
        """
        Set a material to the simulation

        :param name: name of the material
        :param eps: epsilon value of the material
        :type name: str
        :type eps: :class:`numpy.ndarray`, shape=(:math:`1` OR :math:`2` OR
                   :math:`9` OR :math:`3\\times3`), dtype=float
        """
        # check to make sure a simulation exists
        self._check_for_sim()

        # check types, raise errors as needed
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        l_eps = self._material_array_check(eps)
        # add the material as requested
        self._S4Sim._SetMaterial(l_name, l_eps)

    def set_lattice(self, basis_vectors):
        """
        Set the basis vectors for a simulation

        :param basis_vectors: pair of vectors specifying the lattice basic
                              vectors
        :type basis_vectors: :class:`numpy.ndarray`,
                             shape= :math:`\\left( 2, 2 \\right)`,
                             dtype=float
        """
        # check to make sure a simulation exists
        self._check_for_sim()

        # make sure the l_bv is correctly sized
        # this may get a bit tricky
        l_bv = np.asarray(basis_vectors, dtype=np.float64)
        if l_bv.ndim not in [0, 2]:
            err_str = ("basis vectors must be a either a single number for a "
                       "1D lattice, or 2-Dimensional array for a 2D lattice")
            raise RuntimeError(err_str)
        if l_bv.ndim == 0:
            # fix to avoid issues in C++
            l_bv = np.array([basis_vectors], dtype=np.float64)
        else:
            if not ((l_bv.shape[0] == 2) and (l_bv.shape[1] == 2)):
                raise RuntimeError("l_bv must be a 2x2 array")
        l_bv = self._sanitize_array(l_bv,
                                    dtype=np.float64,
                                    warn_name="basis_vectors")

        # pass into the function
        self._S4Sim._SetLattice(l_bv)

    def set_num_g(self, n):
        """
        Set the maximum number of in-plane (x and y) Fourier expansion orders
        to use.

        Computation time is roughly proportional to the cube of this number,
        memory usage approximately the square.

        :param n: number of Fourier expansion orders to use
        :type n: int
        """
        # check to make sure a simulation exists
        self._check_for_sim()

        if not isinstance(n, int):
            print("input n is not an int. Casting to int")
            n = int(n)
            print("using a value of n = {}".format(n))
        if (n < 1):
            raise RuntimeError("n must be >= 1")
        self._S4Sim._SetNumG(n)

    def get_num_g(self):
        """
        Get the current number of Fourier expansion orders

        :return: n
        :type: int
        """

        self._check_for_sim()

        n = self._S4Sim._GetNumG()
        return n

    def add_layer(self, name, thickness, background):
        """
        Add a layer to your simulation object

        :param name: Name of the layer
        :param thickness: thickness of the layer (in scaled units)
        :param background: background material for the layer
        :type name: str
        :type thickness: float
        :type background: str
        """
        self._check_for_sim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        if not isinstance(thickness, float):
            warn_str = ("Warning: thickness not a float; "
                        "attempting to cast to float")
            warnings.warn(warn_str)
            l_thickness = float(thickness)
            print("Using thickness = {}".format(l_thickness))
        else:
            l_thickness = thickness
        if not isinstance(background, str):
            raise RuntimeError("background must be str")
        else:
            l_background = background

        # call the function
        self._S4Sim._AddLayer(l_name, l_thickness, l_background)

    def set_layer(self, name, thickness, background):
        """
        Updates an existing layer with a new thickness and removes all layer
        patterning. If no matching layer is found, adds a new upatterned layer
        with specified thickness and material

        :param name: Name of the layer
        :param thickness: thickness of the layer (in scaled units)
        :param background: background material for the layer
        :type name: str
        :type thickness: float
        :type background: str
        """
        self._check_for_sim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        if not isinstance(thickness, float):
            warn_str = ("Warning: thickness not a float; "
                        "attempting to cast to float")
            warnings.warn(warn_str)
            l_thickness = float(thickness)
            print("Using thickness = {}".format(l_thickness))
        else:
            l_thickness = thickness
        if not isinstance(background, str):
            raise RuntimeError("background must be str")
        else:
            l_background = background

        # call the function
        self._S4Sim._SetLayer(l_name, l_thickness, l_background)

    def set_layer_thickness(self, name, thickness):
        """
        Set the thickness of layer. Layer must exist and thickness must be
        non-negative.

        :param name: Name of the layer
        :param thickness: thickness of the layer (in scaled units)
        :type name: str
        :type thickness: float
        """
        self._check_for_sim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        if not isinstance(thickness, float):
            warn_str = ("Warning: thickness not a float; "
                        "attempting to cast to float")
            warnings.warn(warn_str)
            l_thickness = float(thickness)
            print("Using thickness = {}".format(l_thickness))
        else:
            l_thickness = thickness
        # call the function
        self._S4Sim._SetLayerThickness(l_name, l_thickness)

    def set_layer_pattern_circle(self, name, material, center, radius):
        """
        Adds a filled circle of a specified material to an existing non-copy
        layer.

        The circle should not intersect any other patterning shapes, but may
        contain or be contained within other shapes.

        :param name: name of layer
        :param material: material circle is made of
        :param center: vector specifying the coordinate of the center of the
                       circle
        :param radius: radius of circle
        :type name: str
        :type material: str
        :type center: :class:`numpy.ndarray`,
                      shape= :math:`\\left( 2, \\right)`,
                      dtype=float
        """
        self._check_for_sim()

        # type checks
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            l_name = name
        if not isinstance(material, str):
            raise RuntimeError("material must be str")
        else:
            l_material = material
        l_center = np.asarray(center)
        if not l_center.ndim == 1:
            raise RuntimeError("Center must be a vector (1D array)")
        if not l_center.shape[0] == 2:
            raise RuntimeError("Center must be a 2 element vector (x, y)")
        l_center = self._sanitize_array(l_center,
                                        dtype=np.float64,
                                        warn_name="center")
        l_radius = radius
        if not isinstance(radius, float):
            print("input radius is not a float. Casting to float")
            l_radius = float(l_radius)
            print("using a value of radius = {}".format(l_radius))
        if l_radius < 0:
            raise RuntimeError("raidus must be positive")
        self._S4Sim._SetLayerPatternCircle(l_name,
                                           l_material,
                                           l_center,
                                           l_radius)

    def set_layer_pattern_ellipse(self, name, material, center, halfwidths,
                                  angle=0.0, use_radians=False):
        """
        Adds a filled ellipse of a specified material to an existing non-copy
        layer.

        The ellipse should not intersect any other patterning shapes, but may
        contain or be contained within other shapes.

        Note: If you are using a 1D lattice, make sure to set both center[1]
              and halfwidths[1] to 0.

        :param name: name of layer
        :param material: material circle is made of
        :param center: vector specifying the coordinate of the center of the
                       circle
        :param halfwidths: halfwidths of the ellipse,
                           :math:`\\left(x, y\\right)`, for unrotated ellipse
        :param angle: angle by which to rotate the shape. Uses degrees unless
                      `use_radians=True`
        :param use_radians: set to `True` to use radians rather than degrees
        :type name: str
        :type material: str
        :type center: :class:`numpy.ndarray`,
                      shape= :math:`\\left(2, \\right)`, dtype=float
        :type halfwidths: :class:`numpy.ndarray`,
                          shape= :math:`\\left(n, \\right)`, dtype=float
        :type angle: float
        :type use_radians: bool
        """

        self._check_for_sim()

        # type checks
        if not isinstance(name, str):
            raise RuntimeError("name must be a str")
        else:
            l_name = name
        if not isinstance(material, str):
            raise RuntimeError("material must be a str")
        else:
            l_material = material
        l_center = np.asarray(center)
        if not l_center.ndim == 1:
            raise RuntimeError("Center must be a vector (1D array)")
        if not l_center.shape[0] == 2:
            raise RuntimeError("Center must be a 2 element vector (x, y)")
        l_center = self._sanitize_array(l_center,
                                        dtype=np.float64,
                                        warn_name="center")
        l_halfwidths = np.asarray(halfwidths)
        if not l_halfwidths.ndim == 1:
            raise RuntimeError("halfwidths must be a 1D array")
        if not l_halfwidths.shape[0] == 2:
            raise RuntimeError("halfwidths must be an array of [x, y]")
        l_halfwidths = self._sanitize_array(l_halfwidths,
                                            dtype=np.float64,
                                            warn_name="halfwidths")

        # there is something strange going on with the ability to rotate the
        # polygon
        # main_lua.c has `S4_real angle = luaL_checknumber(L, 5) / 360.;`
        # implying that somehow the input angle is divided into a fraction of
        # a full rotation
        # rather than something like radians
        # It is an angle fraction, so we will handle here, not buried in C++
        l_angle = angle
        if use_radians:
            l_angle /= (np.pi / 2.0)
        else:
            l_angle /= 360.0

        self._S4Sim._SetLayerPatternEllipse(l_name,
                                            l_material,
                                            l_center,
                                            l_angle,
                                            l_halfwidths)

    def set_layer_pattern_rectangle(self, name, material, center, halfwidths,
                                    angle=0.0, use_radians=False):
        """
        Adds a filled rectangle of a specified material to an existing
        non-copy layer.

        The rectangle should not intersect any other patterning shapes, but
        may contain or be contained within other shapes.

        Note: If you are using a 1D lattice, make sure to set both center[1]
              and halfwidths[1] to 0.

        :param name: name of layer
        :param material: material circle is made of
        :param center: vector specifying the coordinate of the center of the
                       circle
        :param halfwidths: halfwidths of the rectangle,
                           :math:`\\left(x,  y \\right)`, for unrotated
                           rectangle
        :param angle: angle by which to rotate the shape. Uses degrees unless
                      `use_radians=True`
        :param use_radians: set to `True` to use radians rather than degrees
        :type name: str
        :type material: str
        :type center: :class:`numpy.ndarray`,
                      shape= :math:`\\left(2,\\right)`, dtype=float
        :type halfwidths: :class:`numpy.ndarray`,
                          shape= :math:`\\left(n,\\right)`, dtype=float
        :type angle: float
        :type use_radians: bool
        """

        self._check_for_sim()

        # type checks
        if not isinstance(name, str):
            raise RuntimeError("name must be a str")
        else:
            l_name = name
        if not isinstance(material, str):
            raise RuntimeError("material must be a str")
        else:
            l_material = material
        l_center = np.asarray(center)
        if not l_center.ndim == 1:
            raise RuntimeError("Center must be a vector (1D array)")
        if not l_center.shape[0] == 2:
            raise RuntimeError("Center must be a 2 element vector (x, y)")
        l_center = self._sanitize_array(l_center,
                                        dtype=np.float64,
                                        warn_name="center")
        l_halfwidths = np.asarray(halfwidths)
        if not l_halfwidths.ndim == 1:
            raise RuntimeError("halfwidths must be a 1D array")
        if not l_halfwidths.shape[0] == 2:
            raise RuntimeError("halfwidths must be an array of [x, y]")
        l_halfwidths = self._sanitize_array(l_halfwidths,
                                            dtype=np.float64,
                                            warn_name="halfwidths")

        # there is something strange going on with the ability to rotate the
        # polygon
        # main_lua.c has `S4_real angle = luaL_checknumber(L, 5) / 360.;`
        # implying that somehow the input angle is divided into a fraction of
        # a full rotation rather than something like radians
        # It is an angle fraction, so we will handle here, not buried in C++
        l_angle = angle
        if use_radians:
            l_angle /= (np.pi / 2.0)
        else:
            l_angle /= 360.0

        self._S4Sim._SetLayerPatternRectangle(l_name,
                                              l_material,
                                              l_center,
                                              l_angle,
                                              l_halfwidths)

    def set_layer_pattern_polygon(self, name, material, center, vertices,
                                  angle=0.0, use_radians=False):
        """
        Adds a filled polygon of a specified material to an existing non-copy
        layer.

        The polygon should not intersect any other patterning shapes, but may
        contain or be contained within other shapes.

        :param name: name of layer
        :param material: material circle is made of
        :param center: vector specifying the coordinate of the center of the
                       circle
        :param vertices: vertices of the polygon. Must be entered in CCW order.
        :param angle: angle by which to rotate the shape. Uses degrees unless
                      `use_radians=True`
        :param use_radians: set to `True` to use radians rather than degrees
        :type name: str
        :type material: str
        :type center: :class:`numpy.ndarray`,
                      shape= :math:`\\left(2,\\right)`, dtype=float
        :type vertices: :class:`numpy.ndarray`,
                        shape= :math:`\\left(n,2\\right)`, dtype=float
        :type angle: float
        :type use_radians: bool

        .. note::

           It is unclear if the vertices are shifted by the center or not.
           It is assumed that they are.
        """

        self._check_for_sim()

        # type checks
        if not isinstance(name, str):
            raise RuntimeError("name must be a str")
        else:
            l_name = name
        if not isinstance(material, str):
            raise RuntimeError("material must be a str")
        else:
            l_material = material
        l_center = np.asarray(center)
        if l_center.ndim != 1:
            raise RuntimeError("Center must be a vector (1D array)")
        if l_center.shape[0] != 2:
            raise RuntimeError("Center must be a 2 element vector (x, y)")
        l_center = self._sanitize_array(l_center,
                                        dtype=np.float64,
                                        warn_name="center")
        l_vertices = np.asarray(vertices)
        if l_vertices.ndim != 2:
            raise RuntimeError("vertices must be a list of vectors (2D array)")
        if l_vertices.shape[1] != 2:
            raise RuntimeError("each vertex must be a 2 element vector (x, y)")
        l_vertices = self._sanitize_array(l_vertices,
                                          dtype=np.float64,
                                          warn_name="vertices")
        # check for CCW
        cverts = np.append(l_vertices, [l_vertices[0]], axis=0)
        cross = np.sum(np.multiply(cverts[:-1, 0], cverts[1:, 1])
                       - np.multiply(cverts[1:, 0], cverts[:-1, 1]))
        if cross < 0:
            err_str = "vertices must be entered in counter-clockwise order"
            raise RuntimeError(err_str)

        # there is something strange going on with the ability to rotate the
        # polygon
        # main_lua.c has `S4_real angle = luaL_checknumber(L, 5) / 360.;`
        # implying that somehow the input angle is divided into a fraction of
        # a full rotation rather than something like radians
        # It is an angle fraction, so we will handle here, not buried in C++
        l_angle = angle
        if use_radians:
            l_angle /= (np.pi / 2.0)
        else:
            l_angle /= 360.0

        self._S4Sim._SetLayerPatternPolygon(l_name,
                                            l_material,
                                            l_center,
                                            l_vertices,
                                            l_angle)

    def set_excitation_planewave(self, angle, pol_s, pol_p,
                                 order=1, use_radians=False):
        """
        Sets the excitation planewave incident upon the front (first specified
        layer) of the structure. If both tilt angles are zero, then the
        planewave is normally incident with the electric field polarized along
        the x-axis for the p-polarization. The phase of each polarization is
        defined at the origin (z=0)

        :param angle: :math:`\\left(\\phi, \\theta\\right)` Angles (in degrees
                      by default. set `use_radians` to `True` to use radians).
                      :math:`\\phi, \\theta` give spherical coordinate angles
                      of the planewave k-vector. :math:`\\phi` specifies the
                      first angle by which :math:`\\left(E,H,k\\right)` should
                      be rotated (CW) about the y-axis. :math:`\\theta`
                      specifies the angle by which :math:`\\left(E,H,k\\right)`
                      should be rotated (CCW) about the z-axis. Note the
                      different directions of rotations for each angle.
        :param pol_s: amplitude, phase (in degrees, set `use_radians` to
                      `True` to use radians) of the s-polarization
        :param pol_p: amplitude, phase (in degrees, set `use_radians` to
                      `True` to use radians) of the p-polarization
        :param order: An optional positive integer specifying which order
                      (mode index) to excite. Defaults to 1.
        :param use_radians: set to `True` to input angles, phases in radians
                            rather than the default degrees
        :type angle: :class:`numpy.ndarray`, shape= :math:`\\left(2, \\right)`,
                     dtype=float
        :type pol_s: :class:`numpy.ndarray`, shape= :math:`\\left(2, \\right)`,
                     dtype=float
        :type pol_p: :class:`numpy.ndarray`, shape= :math:`\\left(2, \\right)`,
                     dtype=float
        :type order: int
        :type use_radians: bool

        .. todo::

           Expand information about :math:`\\theta, \\phi`
        """
        self._check_for_sim()

        # check types
        l_angle = np.asarray(angle)
        if not l_angle.ndim == 1:
            raise RuntimeError("Angle must be a vector (1D array)")
        if not l_angle.shape[0] == 2:
            raise RuntimeError("Angle must be a 2 element vector (phi, theta)")
        l_angle = self._sanitize_array(l_angle,
                                       dtype=np.float64,
                                       warn_name="angle")

        l_pol_s = np.asarray(pol_s)
        if not l_pol_s.ndim == 1:
            raise RuntimeError("pol_s must be a vector (1D array)")
        if not l_pol_s.shape[0] == 2:
            err_str = "pol_s must be a 2 element vector (amplitude, phase)"
            raise RuntimeError(err_str)
        l_pol_s = self._sanitize_array(l_pol_s,
                                       dtype=np.float64,
                                       warn_name="pol_s")

        l_pol_p = np.asarray(pol_p)
        if not l_pol_p.ndim == 1:
            raise RuntimeError("pol_p must be a vector (1D array)")
        if not l_pol_p.shape[0] == 2:
            err_str = "pol_p must be a 2 element vector (amplitude, phase)"
            raise RuntimeError(err_str)
        l_pol_p = self._sanitize_array(l_pol_p,
                                       dtype=np.float64,
                                       warn_name="pol_p")

        l_order = order
        if not isinstance(order, int):
            print("input order is not an int. Casting to int")
            l_order = int(order)
            print("using a value of order = {}".format(l_order))
        if l_order < 1:
            raise RuntimeError("order must be <= 1")

        # convert to radians as required
        if not use_radians:
            # convert phi, theta
            l_angle[0] *= (np.pi/180.0)
            l_angle[1] *= (np.pi/180.0)
            # convert the polarization
            l_pol_s[1] *= (np.pi/180.0)
            l_pol_p[1] *= (np.pi/180.0)

        # call the C++ function
        self._S4Sim._SetExcitationPlaneWave(l_angle, l_pol_s, l_pol_p, l_order)

    def set_frequency(self, freq_r, freq_i=0.0):
        """
        Set the operating frequency of the system (and excitation)

        :param freq_r: The real frequency. This is not the angular frequency
                       :math:`(2 \\pi \\nu_r)`
        :param freq_i: The imaginary frequency of the system. Typically not
                       specified and defaults to zero. If specified, must be
                       negative
        """
        self._check_for_sim()

        l_freq_r = freq_r
        if not isinstance(freq_r, float):
            print("freq_r is not a float. Casting to float")
            l_freq_r = float(l_freq_r)
            print("using a value of freq_r = {}".format(l_freq_r))
        if not freq_i <= 0:
            raise RuntimeError("freq_i must be <= 0")
        l_freq_i = freq_i
        if not isinstance(freq_i, float):
            print("freq_i is not a float. Casting to float")
            l_freq_i = float(l_freq_i)
            print("using a value of freq_i = {}".format(l_freq_i))
        self._S4Sim._SetFrequency(l_freq_r, l_freq_i)

    # Settings for Fourier Modal Methods

    def use_discretized_epsilon(self, use=True):
        """
        Enables or disables the use of discretization in generating the Fourier
        coefficients of the in-plane epsilon profiles, instead of using values
        from closed-form equations. When enabled, the coefficients are obtained
        by FFT.

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))
        self._S4Sim._UseDiscretizedEpsilon(l_use)

    def use_subpixel_smoothing(self, use=True):
        """
        Enables or disables the use of second-order accurate epsilon averaging
        rules within a pixel. The average epsilon within a pixel is computed
        using the fill factor of each material and the interface direction.

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))
        self._S4Sim._UseSubpixelSmoothing(l_use)

    def use_lanczos_smoothing(self, use=True):
        """
        Enables or disables smoothing of the Fourier series representations of
        the layer dielectric constants using the Lanczos sigma factor
        (box filtering). This reduces the Gibbs phenomenon ringing in the real
        space reconstruction.

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))
        self._S4Sim._UseLanczosSmoothing(l_use)

    def use_polarization_decomposition(self, use=True):
        """
        Enables of disables the use of proper in-plane Fourier factorization
        rules by decomposing fields into a polarization basis which conforms
        to the material boundaries. The polarization basis field is
        generated automatically by computing a quasi-harmonic vector field
        everywhere tangent to the layer pattern boundaries. This option is
        not guaranteed to work in the presence of tensor dielectric constants

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))
        self._S4Sim._UsePolarizationDecomposition(l_use)

    def use_jones_vector_basis(self, use=True):
        """
        This option only has an effect with
        :meth:`S4.Simulation.UsePolarizationDecomposition`.
        When enabled, a Jones bector basis field is used intead of a conformal
        harmonic field. Enabling this feature may improve convergence with
        respect to the number of G-vectors.

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))

        self._S4Sim._UseJonesVectorBasis(l_use)

    def use_normal_vector_basis(self, use=True):
        """
        This option only has an effect with UsePolarizationDecomposition().
        When enabled, the resulting vector field is normalized. Where the
        vector field is zero, the unit vector in the x-direction is used.
        Enabling this feature may improve convergence with respect to the
        number of G-vectors.

        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))

        self._S4Sim._UseNormalVectorBasis(l_use)

    def use_experimental_FMM(self, use=True):
        """
        :param use: set to `True` to enable
        :type use: bool
        """
        self._check_for_sim()

        l_use = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            l_use = bool(use)
            print("using value for use = {}".format(l_use))

        self._S4Sim._UseExperimentalFMM(l_use)

    def set_resolution(self, resolution=8):
        """
        Set the resolution of the system. Lots of notes here.

        :param resolution: integer multiple to multiply the largest G-vector by
                           (must be 2 to satisfy the Nyquist limit)
        :type resolution: int
        """
        self._check_for_sim()

        l_resolution = resolution
        if not isinstance(resolution, int):
            print("resolution is not an integer; attempting to cast")
            l_resolution = int(resolution)
            print("using a value of resolution = {}".format(resolution))
        self._S4Sim._SetResolution(l_resolution)

    def get_poynting_flux(self, layer, offset=0.0):
        """
        Get the Poynting Flux

        :param layer: name of layer
        :param offset: offset from the beginning of the layer
        :type layer: str
        :type offset: float

        :return: power flux [forward_real, backward_real,
                 forward_imaginary, backward_imaginary]
        :type: :class:`numpy.ndarray`, shape= :math:`\\left(4, \\right)`,
               dtype=float

        .. todo::

           fix issue with (print(S.GetPoyntingFlux(<layer>))) that
           results in a malloc error; may be alright. Be on the lookout.
        """
        self._check_for_sim()

        if not isinstance(layer, str):
            raise RuntimeError("Layer must be a string")
        l_layer = layer

        l_offset = offset
        if not isinstance(offset, float):
            print("offset should be a float; attempting to cast")
            l_offset = float(offset)
            print("using a value of offset = {}".format(l_offset))

        # get the data
        powerFlux = self._S4Sim._GetPoyntingFlux(l_layer, l_offset)
        return powerFlux

    def get_poynting_flux_by_G(self, layer, offset=0.0):
        """
        Get the Poynting Flux by each wave vector

        :param layer: name of layer
        :param offset: offset from the beginning of the layer
        :type layer: str
        :type offset: float

        :return: power flux [[forward_real, backward_real,
                 forward_imaginary, backward_imaginary]]
        :type: :class:`numpy.ndarray`, shape= :math:`\\left(n, 4, \\right)`,
               dtype=float

        .. todo::

           fix issue with (print(S.GetPoyntingFlux(<layer>))) that
           results in a malloc error; may be alright. Be on the lookout.
        """
        self._check_for_sim()

        if not isinstance(layer, str):
            raise RuntimeError("Layer must be a string")
        l_layer = layer

        l_offset = offset
        if not isinstance(offset, float):
            print("offset should be a float; attempting to cast")
            l_offset = float(offset)
            print("using a value of offset = {}".format(l_offset))

        # get the data
        powerFluxRaw = self._S4Sim._GetPoyntingFluxByG(l_layer, l_offset)
        powerFlux = np.copy(powerFluxRaw.reshape((-1, 4)))
        return powerFlux

    def get_field_at_point(self, point):
        """
        Get the electric and magnetic field at a particular point in the
        structure

        :param point: :math:`\\left(x, y, z, \\right)` point in the structure
                      at which to retrieve the value of the electric field
        :type point: :class:`numpy.ndarray`, shape= :math:`\\left(3, \\right)`,
                     dtype=float

        :return: complex electric and magnetic field vector at specified point
                 :math:`\\left( \\left[ E_x, E_y, E_z \\right], \\left[ H_x,
                 H_y, H_z \\right] \\right)`
        :type: :class:`numpy.ndarray`, shape= :math:`\\left(2, 3 \\right)`,
               dtype=complex
        """

        self._check_for_sim()

        # check that point is valid
        l_point = np.asarray(point)
        if not l_point.ndim == 1:
            raise RuntimeError("Point must be a vector (1D array)")
        if not l_point.shape[0] == 3:
            raise RuntimeError("Point must be a 3 element vector (x, y, z)")
        l_point = np.require(l_point, dtype=np.float64, requirements=["C"])

        # get the data
        raw_field = self._S4Sim._GetFieldAtPoint(point)

        # reshape
        e_field_real = raw_field[0:3]
        e_field_imag = raw_field[3:6]
        h_field_real = raw_field[6:9]
        h_field_imag = raw_field[9:12]

        e_field = e_field_real + 1j * e_field_imag
        h_field = h_field_real + 1j * h_field_imag
        e_field = np.ascontiguousarray(e_field, dtype=np.complex128)
        h_field = np.ascontiguousarray(e_field, dtype=np.complex128)

        return e_field, h_field

    def get_field_plane(self, z, n_uv):
        """
        Get the electric and magnetic field as a grid at a particular z
        coordinate. This is more efficient than get_field_at_point().

        :param z: the :math:`z`-coordinate of the plane on which to obtain
                  the field
        :type z: float
        :param n_uv:
        :type n_uv: :class:`numpy.ndarray`, shape= :math:`\\left(2 \\right)`,
                    dtype=float

        :return: complex electric and magnetic field vector at specified point
                 :math:`\\left( \\left[ E_x, E_y, E_z \\right], \\left[ H_x,
                 H_y, H_z \\right] \\right)`
        :type: :class:`numpy.ndarray`, shape= :math:`\\left(n_uv[1], n_uv[0],
               3 \\right)`, dtype=complex
        """

        self._check_for_sim()

        # check that the z is valid
        try:
            l_z = float(z)
        except Exception as e:
            print("attempted to convert z to a float and failed.")
            raise e
        # check that n_uv is valid
        l_n_uv = np.asarray(n_uv)
        if not l_n_uv.ndim == 1:
            raise RuntimeError("n_uv must be a vector (1D array)")
        if not l_n_uv.shape[0] == 2:
            raise RuntimeError("n_uv must be a 2 element vector (nu, nv)")
        # recast n_uv
        l_n_uv = np.require(l_n_uv, dtype=np.int64, requirements=["C"])
        # compute and return the e, h fields
        efield, hfield = self._S4Sim._GetFieldPlane(l_z, l_n_uv)
        # reshape the nu*nv*3 array into 3D array
        efield = efield.reshape(l_n_uv[1], l_n_uv[0], 3)
        hfield = hfield.reshape(l_n_uv[1], l_n_uv[0], 3)
        # return the arrays
        return efield, hfield

    def get_waves(self, layer):
        """
        Get the Waves

        :param layer: name of layer
        :type layer: str

        :return: waves [forward_real, backward_real,
                 forward_imaginary, backward_imaginary]
        :type: :class:`numpy.ndarray`, shape= :math:`\\left(4, \\right)`,
               dtype=float

        .. todo::

           fix issue with (print(S.GetPoyntingFlux(<layer>))) that
           results in a malloc error; may be alright. Be on the lookout.

           Update documentation:
           a wave object is:
           direction = {kx,ky,kzr,kzi}
           polarization = {x,y,z}
           cu = {re,im}
           cv = {re,im}
        """
        self._check_for_sim()

        if not isinstance(layer, str):
            raise RuntimeError("Layer must be a string")
        l_layer = layer

        # get the data
        rawWaves = self._S4Sim._GetWaves(l_layer)
        # reformat the waves
        waves = np.copy(rawWaves.reshape((-1, 2, 11)))
        return waves

    def _test(self):

        x = self._S4Sim._TestArray()
        return x
