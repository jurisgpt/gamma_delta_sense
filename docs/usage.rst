Usage
=====

Basic Commands
-------------

1. **Initialize the knowledge base**::

    gamma_delta_sense init

2. **Monitor for changes**::

    gamma_delta_sense monitor

3. **Run a one-time scan**::

    gamma_delta_sense scan

4. **View the current status**::

    gamma_delta_sense status

Configuration
------------
The system is configured via the `sense_config.yaml` file in the root directory. See the :doc:`configuration` page for details.

Command Line Interface
---------------------

.. argparse::
   :module: scripts.sense_changes
   :func: get_parser
   :prog: gamma_delta_sense
   :nodescription:
