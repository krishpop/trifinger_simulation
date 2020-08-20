********************************************************************************
Operation through Real Robot Interface
********************************************************************************

Instead of directly using the Python interface, as described :doc:`here <./simvsreal>`,
there is another mode of operation, which is closer to the real robot: 
We can use the whole software infrastructure used for the real robot,
but instead of running the real-robot backend, we replace
it with a simulation backend (see the 
`project site <https://sites.google.com/view/trifinger>`_ 
and links therein to learn about the software infrastructure
of the real robot).
This means that in both cases the same frontend will be used,
hence one can take code written for the real robot (e.g. 
`this demo <https://github.com/open-dynamic-robot-initiative/robot_fingers/blob/master/demos/demo_trifingeredu.py>`_) 
and simply replace the real robot backend with the simulation 
backend or vice versa.

The disadvantage of this mode of operation is that the entire
software infrastructure needs to be installed and compiled
(as detailed in the installation instructions),
and that one is not able to use simulation-specific functions.

It is also possible to use this simulation through our software for interfacing with the
real robot. So, you could
access the real TriFinger with the simulation as seen in :doc:`simwithreal`.
You can also access the simulated TriFinger through the real interface, as seen here below.


Creating a Simulation Backend
===========================================================



To create a TriFinger backend using simulation:

.. code-block:: python

    import trifinger_simulation.drivers

    backend = trifinger_simulation.drivers.create_trifinger_backend(
        robot_data, real_time_mode=True, visualize=True
    )

If ``real_time_mode`` is ``True``, the backend will expect a new action every
millisecond and repeat the previous action if it is not provided in time (like
on the real robot).  If set to ``False``, it will run as fast as possible and
wait for new actions.

Set ``visualize=True`` to run the pyBullet GUI for visualization.


For a complete example, see `demo_robot_interface.py`_

.. _`demo_robot_interface.py`: https://github.com/open-dynamic-robot-initiative/trifinger_simulation/blob/master/demos/catkin/demo_robot_interface.py
.. _`robot_interfaces`: https://github.com/open-dynamic-robot-initiative/robot_interfaces