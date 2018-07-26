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
            print("input raidus is not a float. Casting to float")
            lRadius = float(lRadius)
            print("using a value of radius = {}".format(lRadius))
        if lRadius < 0:
            raise RuntimeError("raidus must be positive")
        self._S4Sim._SetLayerPatternCircle(lName, lMaterial, lCenter, lRadius)
