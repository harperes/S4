Tutorial
========

Basic usage
-----------

To use |S4|, you may run it interactively in a python REPL environment (such as iPython), or using a
python script. The basic flow of a script is listed below.
To find more information about these functions and for a full listing, see the :ref:`python-api-label`.

1. Obtain a new simulation object::

    S = S4.Simulation()
    S.create_new()

  S now contains a simulation object with a blank specification, and no solutions.

2. Set the lattice and number of basis functions::

    S.set_lattice([[a_x, a_y], [b_x, b_y])
    S.set_num_g(100)

This sets the periodicity based on the lattice vectors
:math:`\left(a_x, a_y \right), \left(b_x, b_y \right)`.
The number of basis functions is set to 100.

3. Define all materials::

    S.add_material('Vacuum', [1.0, 0.0])
    S.add_materials('Silicon', [12, 0.01])

  This adds a material called "Vacuum" with a dielectric constant of 1, and a material called "Silicon", with a dielectric constant of :math:`12+0.01i`

4. Add all layers::

    S.add_layer('top', 0, 'Vacuum')
    S:add_layer('slab', 0.5, 'Silicon')
    S:add_layer('bottom', 0, 'Vacuum')

  Here we are adding a semi-infinite Vacuum layer (the thickness is largely irrelevant), a middle slab layer made of silicon with a thickness of 0.5, and finally a bottom semi-infinite Vacuum layer.

  .. todo::

     Investigate if it is always preferable to copy layers if possible since it reduces the computational cost.

  .. todo::

     Investigate if copy functions have been ported

5. Add patterning to layers::

    S.set_layer_pattern_circle('slab',   -- layer to pattern
                               'Vacuum', -- material inside circle
                               [0,0],    -- center of circle
                               0.2)      -- radius of circle

  This creates a cylinder of radius :math:`r=0.2` to the middle layer.

6. Specify the excitation mechanism::

    S.set_excitation_planewave(
        [0, 0], -- phi in [0,180), theta in [0,360)
        [1, 0], -- s-polarization amplitude and phase in degrees
        [0, 0]) -- p-polarization

  This sets the excitation to a normally incident planewave with amplitude 1.

7. Specify the operating frequency::

    S.set_frequency(0.4)

8. Obtain desired output::

    transmission = S.get_poynting_flux('bottom')
    print(transmission)

  This obtains the forward power flux in the bottom layer, which is also the transmitted power.

Typical usage
-------------

The only fully supported front end is the :doc:`Python API <python_api>`. The original Lua API is not
supported by these developers.
Most users are interested in computing frequency (or wavelength) spectra, in which case
:meth:`S4.Simulation.set_frequency` is called in a loop over frequency.
Putting :meth:`S4.Simulation.get_poynting_flux` afterwards in the same loop allows obtaining reflection/transmission/absorption power spectra.
If the materials used are dispersive, then :meth:`S4.Simulation.set_material` must also be called
within the loop before the call to :meth:`S4.Simulation.get_poynting_flux` to update material
constants for each new frequency.

When running parameter sweeps for optimizing structures, a number of structural parameters are
typically varied, such as lattice constants, layer thicknesses, and patterning dimensions.
Due to the way in which |S4| performs lazy computation (things are not computed or recomputed
until they are required), the order of nested loops matters greatly.
In general, all output quantities for a given structure should be computed at once before
modifying the structure, since structure modification changes the solution completely.
Next, layer thicknesses can be changed without requiring recomputation of layer eigenmodes.
A slightly more computationally expensive modification is changing a layer's patterning,
which requires recomputing the layer's eigenmodes.
Changing material properties invalidates eigenmodes of any layer using the material.
Finally, changes in lattice constant, frequency, and incidence angles require a complete
recomputation of the solution.

.. _fmm-formulations-label:

Fourier Modal Method formulations
---------------------------------

There has been extensive literature on the best way to generate the Fourier series coefficients for
the in-plane dielectric profiles of each layer. |S4| implements a number of different formulations.
The following functions determine which formulation is selected:

* :meth:`S4.Simulation.use_discretized_epsilon`
* :meth:`S4.Simulation.use_polarization_decomposition`
* :meth:`S4.Simulation.use_subpixel_smoothing`
* :meth:`S4.Simulation.use_jones_vector_basis`
* :meth:`S4.Simulation.use_normal_vector_basis`

In addition, the following functions control accuracy and the lattice truncation:

* :meth:`S4.Simulation.set_resolution`
* :meth:`S4.Simulation.set_lattice_truncation`

To simplify the choice for users, the table below summarizes the recommended settings. It is recommended to always use circular truncation unless there is a good reason to do otherwise. Speed indicates the speed of the Fourier coefficient generation, which is usually not the dominant part of the simulation time.

+-----------------+-------------------------+------------------------+--------+----------+
| Options         | Can handle Anisotropic? | Recommended resolution | Speed  | Accuracy |
+=================+=========================+========================+========+==========+
| none            | yes                     | N/A                    | fast   | poor     |
+-----------------+-------------------------+------------------------+--------+----------+
| Disc            | yes                     | 8                      | medium | poor     |
+-----------------+-------------------------+------------------------+--------+----------+
| Subpixel        | yes                     | 4                      | medium | medium   |
+-----------------+-------------------------+------------------------+--------+----------+
| Pol             | no                      | 8                      | slow   | good     |
+-----------------+-------------------------+------------------------+--------+----------+
| Pol+Normal      | no                      | 8                      | slow   | good     |
+-----------------+-------------------------+------------------------+--------+----------+
| Pol+Jones       | no                      | 8                      | slow   | good     |
+-----------------+-------------------------+------------------------+--------+----------+
| Disc+Pol        | no [#f1]_               | 4                      | slow   | medium   |
+-----------------+-------------------------+------------------------+--------+----------+
| Disc+Pol+Normal | no [#f1]_               | 4                      | slow   | medium   |
+-----------------+-------------------------+------------------------+--------+----------+
| Disc+Pol+Jones  | no [#f1]_               | 4                      | slow   | medium   |
+-----------------+-------------------------+------------------------+--------+----------+

It is recommended that users use the default (no options) despite the poor accuracy, since the polarization basis settings can introduce spurious regions of gain into the material patterning. This may or may not be a problem for some users using extremely lossy metals, but for low loss metals, typically energy conservation is violated.

.. rubric:: Footnotes

.. [#f1] The formulation does not strictly work correctly for anisotropic media however it may still work. Proper support for anisotropic materials is in principle possible. There are currently no plans for implementing generation of the proper basis fields for this feature.

Examples
--------

The source distribution of |S4| includes numerous fully working didactic examples as well as examples replicating published results.
You can find these examples in the ``examples/`` directory of the source distribution.

.. |S4| replace:: S\ :sup:`4`
