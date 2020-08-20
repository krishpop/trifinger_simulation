.. _sec-simulation-vs-real-robot:

********************************************************
Direct Operation
********************************************************

It is possible to directly use the ``SimFinger`` class in Python, without
passing through the entire software infrastructure (as described :doc:`here <./realwithsim>`).
This is convenient as it does not require installing the entire real robot software,
and one has access to the extra functionality available in simulation which does
not exist on the real robot. 


While the ``SimFinger`` interface is largely identical to 
the real robot interface (`robot_interfaces::RobotFrontend`_),
there are some small differences explained below.


Hence, for developing this is the recommended mode, while operation
through the real robot software is convenient for testing before executing code on the real robot.


Main Differences
=====================================================

- On the real robot, it is possible to pass a time index that lies in the future
  and most methods of the `robot_interfaces::RobotFrontend`_ will simply block and wait until this
  time step is reached.  The simulation, however, is not running asynchronously
  but is actively stepped every time ``append_desired_action()`` is called.
  Therefore the behaviour of waiting for a time step is not supported.  Instead,
  passing a time index that lies in the future will result in an error.
- In SimFinger, there is no actual time series.  The API in the simulation
  follows the same principle to make the transition to the real robot easier.
  However, it is implemented with a buffer size of 1, so the getter methods only
  provide data for the current time step.
- Unlike on the real robot, here it is possible to access information from *t + 1*.  In a typical gym
  environment, it is expected that the observation returned by ``step(action)``
  belongs to the moment *after* the given action is executed (this corresponds
  to the time index *t + 1*).  To make it easier to get started, we therefore
  allow to access the observations of this time index in the simulation.


.. Simulation is stepped in ``append_desired_action()``
.. ========================================================

.. The simulation is explicitly stepped in the ``append_desired_action()``
.. method: this is because the simulation doesn't exhibit real-time
.. behaviour. So, every time the ``append_desired_action()`` is called,
.. the simulation is stepped, and the next time step in the simulation is computed.
.. This means that the state of the simulation does not change as long as this
.. method is not called. This is different than on the real robot, which will physically
.. continue to move and will repeat the last action if no new action is provided in time.


.. TODO: it should be explained here also that in simulation you can access one timestep into the future.






.. .. _`No waiting for future time steps`:


.. No waiting for future time steps
.. ======================================

.. On the real robot, it is possible to pass a time index that lies in the future
.. and most methods of the `robot_interfaces::RobotFrontend`_ will simply block and wait until this
.. time step is reached.  The simulation, however, is not running asynchronously
.. but is actively stepped every time ``append_desired_action()`` is called.
.. Therefore the behaviour of waiting for a time step is not supported.  Instead,
.. passing a time index that lies in the future will result in an error.


.. No Time Series in SimFinger
.. ==============================

.. The `robot_interfaces`_ package makes use of time series for observations,
.. actions, etc.  This means all data of the last few time steps is available.  One
.. could, for example do the following to determine how the state of the robot
.. changed:

.. .. code-block:: python

..     previous_observation = frontend.get_observation(t - 1)
..     current_observation = frontend.get_observation(t)

.. The ``SimFinger`` class does not implement a time series, so it only provides
.. the observation of the current time step ``t``.  Passing any other value for
.. ``t`` will result in an error.


API-differences with `robot_interfaces::RobotFrontend`_
=========================================================

.. Our goal is to provide the same API in ``SimFinger`` as in ``RobotFrontend`` to
.. make transition between simulation and real robot easy.  There are a few
.. differences, though.

Currently ``SimFinger`` supports the following methods:

- ``append_desired_action()``
- ``get_observation()``
- ``get_desired_action()``
- ``get_applied_action()``
- ``get_timestamp_ms()``
- ``get_current_timeindex()``

The following methods are not supported:

- ``get_status()``:  There are no meaningful values for the status message in
  simulation, so this method is omitted to avoid confusion.
- ``wait_until_timeindex()``:  In general the process of waiting for a specific
  time step is not supported, see :ref:`No waiting for future time steps`.

.. _`robot_interfaces::RobotFrontend`: https://github.com/open-dynamic-robot-initiative/robot_interfaces/blob/master/include/robot_interfaces/robot_frontend.hpp
.. _`robot_interfaces`: https://github.com/open-dynamic-robot-initiative/robot_interfaces/blob/master/include/robot_interfaces/
