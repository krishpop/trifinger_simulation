*************************************************
Welcome to the TriFinger Robot Simulation Documentation
*************************************************



+--------------------------------------+--------------------------------+
|.. _edu:                              |.. _one:                        |
|                                      |                                |
|.. figure:: images/multi_object.JPG   |.. figure:: images/edu.png      |
|   :width: 95 %                       |   :width: 95 %                 |
|   :align: center                     |   :align: center               |
|                                      |                                |
+--------------------------------------+--------------------------------+

This package provides a simulation of to the TriFinger robots 
using the `pybullet physics engine <https://pypi.org/project/pybullet/>`_.

To Learning more about the TriFinger robots, check out our official `project website`_, and the paper_
of this work.

.. note::

   The Real Robot Challenge is currently in progress! Please refer to the official site of the
   `Real Robot Challenge <https://real-robot-challenge.com/>`_  for more details.
   Also, note that this is *not* the challenge simulator. The challenge simulator can be found on
   `rrc_simulation`_.


Overview
=============================================
The user interface of this package was designed to be identical
to the interface to the real robot. Therefore, to understand the logic of 
the present package, it is necessary 
to first read the about the logic of the real-robot interface 
in the `documentation <https://open-dynamic-robot-initiative.github.io/code_documentation/robot_interfaces/docs/doxygen/html/md_docs_timeseries.html>`_
and the paper_.


The main components of this package are:

1. The ``SimFinger`` class: which implements the complete simulation environment for the TriFinger, including all
   methods to control it, interact with it, to set its properties, as well as to setup the world around it.
   For more details on this class, check out :doc:`../api/sim_finger` (API doc).

2. The ``TriFingerPlatform`` class: which is a wrapper around ``SimFinger`` to provide a similar API as that of the
   real TriFinger platform. For more details on this, please refer to :doc:`../api/trifingerplatform` (API doc),
   and the docs in :ref:`sim-real`.

3. A gym-wrapper with two basic environments: for reaching ("TriFingerReach-v0"), and for pushing ("TriFingerPush-v0"),
   and an environment that you can use to perform tasks of varying
   difficulty levels involving manipulation of a cubical object ("TriFingerCubeDifficulty{}-v1"), where the difficulty values could be one of {1, 2, 3, 4}. This environment is from
   the `Real Robot Challenge <https://real-robot-challenge.com/>`_ . For more details on this, please refer `here <https://people.tuebingen.mpg.de/felixwidmaier/realrobotchallenge/simulation_phase/tasks.html>`_.






.. toctree::
   :maxdepth: 2
   :caption: Installation

   getting_started/installation


.. toctree::
   :maxdepth: 1
   :caption: Modes of Operation
   
   simreal/simvsreal
   simreal/realwithsim

.. toctree::
   :maxdepth: 1
   :caption: Examples
   
   getting_started/demos
   simreal/simwithreal
   .. simreal/timesteplogic

.. toctree::
   :maxdepth: 1
   :caption: API Documentation

   The SimFinger Class <api/sim_finger>
   The TriFingerPlatform Class <api/trifingerplatform>


.. toctree::
   :maxdepth: 1
   :caption: TriFinger Versions

   getting_started/trifinger_versions



Indices and tables
==================

* :ref:`genindex`

.. raw:: html

   <div style='text-align: center; margin-bottom: 2em;'>
   <iframe width="560" height="315" src="https://www.youtube.com/embed/xu5VvyjDLRY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
   </iframe>
   </div>

Citation
==============

If you are using this package in your academic work,
please cite this repository and also the corresponding paper:

.. code-block:: bibtex

   @misc{trifinger-simulation,
      author = {Joshi, Shruti and Widmaier, Felix and Agrawal, Vaibhav and Wüthrich, Manuel},
      year = {2020},
      publisher = {GitHub},
      journal = {GitHub repository},
      howpublished = {\url{https://github.com/open-dynamic-robot-initiative/trifinger_simulation}},
   }

.. code-block:: bibtex

   @misc{wthrich2020trifinger,
      title={TriFinger: An Open-Source Robot for Learning Dexterity},
      author={Manuel Wüthrich and Felix Widmaier and Felix Grimminger and Joel Akpo and Shruti Joshi and Vaibhav Agrawal and Bilal Hammoud and Majid Khadiv and Miroslav Bogdanovic and Vincent Berenz and Julian Viereck and Maximilien Naveau and Ludovic Righetti and Bernhard Schölkopf and Stefan Bauer},
      year={2020},
      eprint={2008.03596},
      archivePrefix={arXiv},
      primaryClass={cs.RO}
   }

.. _package: https://github.com/open-dynamic-robot-initiative/trifinger_simulation
.. _`project website`: https://sites.google.com/view/trifinger
.. _paper: https://arxiv.org/abs/2008.03596
.. _`Real Robot Challenge`: https://people.tuebingen.mpg.de/felixwidmaier/realrobotchallenge/
.. _`rrc_simulation`: https://github.com/rr-learning/rrc_simulation
