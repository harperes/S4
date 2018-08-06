# from ._S4 import S4_Simulation
from ._S4 import S4_Simulation as _S4Sim
import numpy as np
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

    def _checkForSim(self):
        """
        Helper function to check to make sure that a simulation object exists;
        otherwise, segmentation faults may occur
        """
        if not self._hasSim:
            raise RuntimeError("No simulation found. Aborting.")

    def CreateNew(self):
        """
        Create a new simulation instance

        """
        self._S4Sim._CreateNew()
        self._hasSim = True

    def _MaterialArrayCheck(self, eps):
        """
        Helper function to check values of the eps array

        :param eps: epsilon value of material
        :type eps: lorem ipsum

        :return: lEPS
        :type: lorem ipsum
        """

        lEPS = np.asarray(eps)
        if lEPS.ndim > 2:
            raise RuntimeError("eps must be a 1- or 2-Dimensional array")
        if lEPS.ndim == 1:
            ndims = [1, 2, 9]
            if not lEPS.shape[0] in ndims:
                raise RuntimeError("the shape of eps must be a 1, 2, or 9 element array")
        elif lEPS.ndim == 2:
            if not (lEPS.shape[0] == 3) and (lEPS.shape[1] == 3):
                raise RuntimeError("eps must be a 3x3 array")
        lEPS = np.require(lEPS, dtype=np.float64, requirements=["C"])
        return lEPS

    def AddMaterial(self, name, eps):
        """
        Add a material to the simulation

        :param name: name of the material
        :param eps: epsilon value of the material
        :type name: :class:`str`
        :type eps: :class:`numpy.ndarray`, shape=(:math:1 OR :math:2 OR math:9 OR math:3x3),
        dtype=:class:`numpy.float`
        """
        # check to make sure a simulation exists
        self._checkForSim()

        # check types, raise errors as needed
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        lEPS = self._MaterialArrayCheck(eps)
        # add the material as requested
        self._S4Sim._AddMaterial(lName, lEPS)

    def SetMaterial(self, name, eps):
        """
        Set a material to the simulation

        :param name: name of the material
        :param eps: epsilon value of the material
        :type name: :class:`str`
        :type eps: :class:`numpy.ndarray`, shape=(:math:1 OR :math:2 OR math:9 OR math:3x3),
        dtype=:class:`numpy.float`
        """
        # check to make sure a simulation exists
        self._checkForSim()

        # check types, raise errors as needed
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        lEPS = self._MaterialArrayCheck(eps)
        # add the material as requested
        self._S4Sim._SetMaterial(lName, lEPS)

    def SetLattice(self, basisVectors):
        """
        Set the basis vectors for a simulation

        :param basisVectors: pair of vectors specifying the lattice basic vectors
        :type basisVectors: :class:`numpy.ndarray`, shape=(:math:`left(2,2)`, dtype=:class:`numpy.float`)
        """
        # check to make sure a simulation exists
        self._checkForSim()

        # make sure the lBV is correctly sized
        lBV = np.asarray(basisVectors)
        if lBV.ndim != 2:
            raise RuntimeError("basis vectors must be a 2-Dimensional array")
        if not ((lBV.shape[0] == 2) and (lBV.shape[1] == 2)):
            raise RuntimeError("lBV must be a 2x2 array")
        lBV = np.require(lBV, dtype=np.float64, requirements=["C"])

        # pass into the function
        self._S4Sim._SetLattice(lBV)

    def SetNumG(self, n):
        """
        Set the maximum number of in-plane (x and y) Fourier expansion orders to use.

        Computation time is roughly proportional to the cube of this number, memory usage
        approximately the square.

        :param n: number of Fourier expansion orders to use
        :type n: int
        """
        # check to make sure a simulation exists
        self._checkForSim()

        if not isinstance(n, int):
            print("input n is not an int. Casting to int")
            n = int(n)
            print("using a value of n = {}".format(n))
        if (n < 1):
            raise RuntimeError("n must be >= 1")
        self._S4Sim._SetNumG(n)

    def GetNumG(self):
        """
        Get the current number of Fourier expansion orders

        :return: n
        :type: int
        """

        self._checkForSim()

        n = self._S4Sim._GetNumG()
        return n

    def AddLayer(self, name, thickness, background):
        """
        Add a layer to your simulation object

        :param name: Name of the layer
        :param thickness: thickness of the layer (in scaled units)
        :param background: background material for the layer
        :type name: str
        :type thickness: float
        :type background: str
        """
        self._checkForSim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        if not isinstance(thickness, float):
            print("Warning: thickness not a float; attempting to cast to float")
            lThickness = float(thickness)
            print("Using thickness = {}".format(lThickness))
        else:
            lThickness = thickness
        if not isinstance(background, str):
            raise RuntimeError("background must be str")
        else:
            lBackground = background

        # call the function
        self._S4Sim._AddLayer(lName, lThickness, lBackground)

    def SetLayer(self, name, thickness, background):
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
        self._checkForSim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        if not isinstance(thickness, float):
            print("Warning: thickness not a float; attempting to cast to float")
            lThickness = float(thickness)
            print("Using thickness = {}".format(lThickness))
        else:
            lThickness = thickness
        if not isinstance(background, str):
            raise RuntimeError("background must be str")
        else:
            lBackground = background

        # call the function
        self._S4Sim._SetLayer(lName, lThickness, lBackground)

    def SetLayerThickness(self, name, thickness):
        """
        Set the thickness of layer. Layer must exist and thickness must be
        non-negative.

        :param name: Name of the layer
        :param thickness: thickness of the layer (in scaled units)
        :type name: str
        :type thickness: float
        """
        self._checkForSim()

        # handle quick error checking
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        if not isinstance(thickness, float):
            print("Warning: thickness not a float; attempting to cast to float")
            lThickness = float(thickness)
            print("Using thickness = {}".format(lThickness))
        else:
            lThickness = thickness
        # call the function
        self._S4Sim._SetLayerThickness(lName, lThickness)

    def SetLayerPatternCircle(self, name, material, center, radius):
        """
        Adds a filled circle of a specified material to an existing non-coy layer.

        The circle should not intersect any other patterning shapes, but may contain
        or be contained within other shapes.

        :param name: name of layer
        :param material: material circle is made of
        :param center: vector specifying the coordinate of the center of the circle
        :param radius: radius of circle
        :type name: str
        :type material: str
        :type center: :class:`numpy.ndarray`, shape=(2,), dtype=:class:`numpy.float`
        """
        self._checkForSim()

        # type checks
        if not isinstance(name, str):
            raise RuntimeError("name must be str")
        else:
            lName = name
        if not isinstance(material, str):
            raise RuntimeError("material must be str")
        else:
            lMaterial = material
        lCenter = np.asarray(center)
        if not lCenter.ndim == 1:
            raise RuntimeError("Center must be a vector (1D array)")
        if not lCenter.shape[0] == 2:
            raise RuntimeError("Center must be a 2 element vector (x, y)")
        lCenter = np.require(lCenter, dtype=np.float64, requirements=["C"])
        lRadius = radius
        if not isinstance(radius, float):
            print("input radius is not a float. Casting to float")
            lRadius = float(lRadius)
            print("using a value of radius = {}".format(lRadius))
        if lRadius < 0:
            raise RuntimeError("raidus must be positive")
        self._S4Sim._SetLayerPatternCircle(lName, lMaterial, lCenter, lRadius)

    def SetExcitationPlaneWave(self, angle, polS, polP, order=1, useRadians=False):
        """
        Sets the excitation planewave incident upon the front (first specified layer)
        of the structure. If both tilt angles are zero, then the planewave is normally
        incident with the electric field polarized along the x-axis for the
        p-polarization. The phase of each polarization is defined at the origin (z=0)

        :param angle: (phi, theta) Angles (in degrees by default. set useRadians to True to use radians). phi, theta give spherical coordiante angles of the planewave k-vector. File in more later.
        :param polS: amplitude, phase (in degrees, set useRadians to True to use radians) of the s-polarization
        :param polP: amplitude, phase (in degrees, set useRadians to True to use radians) of the p-polarization
        :param order: An optional positive integer specifying which order (mode index) to excite. Defaults to 1.
        :param useRadians: set to True to input angles, phases in radians rather than the default degrees
        :type angle: :class:`numpy.ndarray`, shape=(2,), dtype=:class:`numpy.float`
        :type polS: :class:`numpy.ndarray`, shape=(2,), dtype=:class:`numpy.float`
        :type polP: :class:`numpy.ndarray`, shape=(2,), dtype=:class:`numpy.float`
        :type order: int
        :type useRadians: bool
        """
        self._checkForSim()

        # check types
        lAngle = np.asarray(angle)
        if not lAngle.ndim == 1:
            raise RuntimeError("Angle must be a vector (1D array)")
        if not lAngle.shape[0] == 2:
            raise RuntimeError("Angle must be a 2 element vector (phi, theta)")
        lAngle = np.require(lAngle, dtype=np.float64, requirements=["C"])

        lPolS = np.asarray(polS)
        if not lPolS.ndim == 1:
            raise RuntimeError("polS must be a vector (1D array)")
        if not lPolS.shape[0] == 2:
            raise RuntimeError("polS must be a 2 element vector (amplitude, phase)")
        lPolS = np.require(lPolS, dtype=np.float64, requirements=["C"])

        lPolP = np.asarray(polP)
        if not lPolP.ndim == 1:
            raise RuntimeError("polP must be a vector (1D array)")
        if not lPolP.shape[0] == 2:
            raise RuntimeError("polP must be a 2 element vector (amplitude, phase)")
        lPolP = np.require(lPolP, dtype=np.float64, requirements=["C"])

        lOrder = order
        if not isinstance(order, int):
            print("input order is not an int. Casting to int")
            lOrder = int(order)
            print("using a value of order = {}".format(lOrder))
        if lOrder < 1:
            raise RuntimeError("order must be <= 1")

        # convert to radians as required
        if not useRadians:
            # convert phi, theta
            lAngle[0] *= (np.pi/180.0)
            lAngle[1] *= (np.pi/180.0)
            # convert the polarization
            lPolS[1] *= (np.pi/180.0)
            lPolP[1] *= (np.pi/180.0)

        # call the C++ function
        self._S4Sim._SetExcitationPlaneWave(lAngle, lPolS, lPolP, lOrder)

    def SetFrequency(self, freqR, freqI=0.0):
        """
        Set the operating frequency of the system (and excitation)

        :param freqR: The real frequency. This is not the angular frequency (2*:math:`\pi`*freqR)
        :param freqI: The imaginary frequency of the system. Typically not specified and defaults to zero. If specified, must be negative
        """
        self._checkForSim()

        lFreqR = freqR
        if not isinstance(freqR, float):
            print("freqR is not a float. Casting to float")
            lFreqR = float(lFreqR)
            print("using a value of freqR = {}".format(lFreqR))
        if not freqI <= 0:
            raise RuntimeError("freqI must be <= 0")
        lFreqI = freqI
        if not isinstance(freqI, float):
            print("freqI is not a float. Casting to float")
            lFreqI = float(lFreqI)
            print("using a value of freqI = {}".format(lFreqI))
        self._S4Sim._SetFrequency(lFreqR, lFreqI)

    # Settings for Fourier Modal Methods

    def UseDiscretizedEpsilon(self, use=True):
        """
        Enables or disables the use of discretization in generating the Fourier
        coefficients of the in-plane epsilon profiles, instead of using values
        from closed-form equations. When enabled, the coefficients are obtained
        by FFT.

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))
        self._S4Sim._UseDiscretizedEpsilon(lUse)


    def UseSubpixelSmoothing(self, use=True):
        """Enables or disables the use of second-order accurate epsilon averaging
        rules within a pixel. The average epsilon within a pixel is computed
        using the fill factor of each material and the interface direction.

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))
        self._S4Sim._UseSubpixelSmoothing(lUse)

    def UseLanczosSmoothing(self, use=True):
        """
        Enables of disables smoothing of the Fourier series representations of
        the layer dielectric constants using the Lanczos sigma factor (box filtering).
        This reduces the Gibbs phenomenon ringing in the real space reconstruction.

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))
        self._S4Sim._UseLanczosSmoothing(lUse)

    def UsePolarizationDecomposition(self, use=True):
        """
        Enables of disables the use of proper in-plane Fourier factorization
        rules by decomposing fields into a polarization basis which conforms
        to the material boundaries. The polarization basis field is
        generated automatically by computing a quasi-harmonic vector field
        everywhere tangent to the layer pattern boundaries. This option is
        not guaranteed to work in the presence of tensor dielectric constants

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))
        self._S4Sim._UsePolarizationDecomposition(lUse)

    def UseJonesVectorBasis(self, use=True):
        """
        This option only has an effect with UsePolarizationDecomposition().
        When enabled, a Jones bector basis field is used intead of a conformal
        harmonic field. Enabling this feature may improve convergence with
        respect to the number of G-vectors.

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))

        self._S4Sim._UseJonesVectorBasis(lUse)

    def UseNormalVectorBasis(self, use=True):
        """
        This option only has an effect with UsePolarizationDecomposition().
        When enabled, the resulting vector field is normalized. Where the
        vector field is zero, the unit vector in the x-direction is used.
        Enabling this feature may improve convergence with respect to the
        number of G-vectors.

        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))

        self._S4Sim._UseNormalVectorBasis(lUse)

    def UseExperimentalFMM(self, use=True):
        """
        :param use: set to True to enable
        :type use: bool
        """
        self._checkForSim()

        lUse = use
        if not isinstance(use, bool):
            print("use is not of type bool; attempting to cast")
            lUse = bool(use)
            print("using value for use = {}".format(lUse))

        self._S4Sim._UseExperimentalFMM(lUse)

    def SetResolution(self, resolution=8):
        """
        Set the resolution of the system. Lots of notes here.

        :param resolution: integer multiple to multiply the largest G-vector by
        (must be 2 to satisfy the Nyquist limit)
        :type resolution: int
        """
        self._checkForSim()

        lRes = resolution
        if not isinstance(resolution, int):
            print("resolution is not an integer; attempting to cast")
            lRes = int(resolution)
            print("using a value of resolution = {}".format(resolution))
        self._S4Sim._SetResolution(lRes)

    def TestArray(self):
        """
        """
        self._checkForSim()
        x = self._S4Sim._TestArray()
        print(x)

    def GetPoyntingFlux(self, layer, offset=0.0):
        """
        Get the Poynting Flux

        :param layer: name of layer
        :param offset: offset from the beginning of the layer
        :type layer: str
        :type offset: float

        :return: power flux [forward_real, backward_real,
        forward_imaginary, backward_imaginary]
        :type: :class:`numpy.ndarray`, shape=(4,), dtype=np.float64

        TODO: fix issue with (print(S.GetPoyntingFlux(<layer>))) that
        results in a malloc error; may be alright. Be on the lookout
        """
        self._checkForSim()

        if not isinstance(layer, str):
            raise RuntimeError("Layer must be a string")
        lLayer = layer

        lOffset = offset
        if not isinstance(offset, float):
            print("offset should be a float; attempting to cast")
            lOffset = float(offset)
            print("using a value of offset = {}".format(lOffset))

        # get the data
        powerFlux = self._S4Sim._GetPoyntingFlux(lLayer, lOffset)
        return powerFlux
