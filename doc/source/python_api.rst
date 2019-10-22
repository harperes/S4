.. default-domain:: py

.. _python-api-label:

Python API reference
====================

|S4| is now accessed as a `Python <http://python.org>`_ package, as we have elected to drop the original `Lua <http://www.lua.org>`_ interface.
The python interface is nearing completion of the original Lua interface. If you discover any missing functionality
(`original Lua API <https://web.stanford.edu/group/fan/S4/lua_api.html>`_, please make an issue on `Github <https://github.com/harperes/S4/issues>`_).

Note on spherical coordinate system
-----------------------------------

The spherical coordinate system used to specify the incident planewave is defined using the "mathematical" nomenclature (as opposed to the "physical" nomenclature). This means the normal vector to the incident planewave is defined by :math:`\left( r=1, \phi, \theta \right)` where :math:`\phi` is the polar (elevation) angle and :math:`\theta` is the azimuthal angle. **This is the opposite of the physical coordinate system.**

Also take care to note that :math:`\phi, \, \theta` are by default defined in degrees instead of radians. You may use radian with the flag `use_radians=True`.

`Please see wikipedia for more information <https://en.wikipedia.org/wiki/Spherical_coordinate_system>`_

S4 module
---------

.. _python-api-S4:

.. currentmodule:: S4

.. autoclass:: Simulation
   :members:

.. |S4| replace:: S\ :sup:`4`
