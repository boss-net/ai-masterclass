Testing
=======

Running Tests
=============

To run all tests:

.. code-block:: bash

    pytest tests/

To run a specific test file:

.. code-block:: bash

    pytest tests/unit/test_models.py

To run tests with coverage:

.. code-block:: bash

    pytest --cov=bosskit tests/

Test Structure
=============

Tests are organized in:

- ``tests/unit/``: Unit tests
- ``tests/integration/``: Integration tests
- ``tests/functional/``: Functional tests

Writing Tests
============

1. Use pytest fixtures for setup/teardown
2. Mock external services
3. Write clear test descriptions
4. Use parameterized tests for similar cases
