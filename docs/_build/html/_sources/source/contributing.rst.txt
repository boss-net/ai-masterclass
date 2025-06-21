Contributing
============

Development Setup
----------------

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/boss-net/ai-masterclass.git
    cd ai-masterclass

2. Create a virtual environment:

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate

3. Install development dependencies:

.. code-block:: bash

    pip install -r requirements/requirements-dev.txt

4. Run tests:

.. code-block:: bash

    pytest tests/

Style Guide
-----------

1. Follow PEP 8 style guide
2. Use type hints
3. Write docstrings for all public functions and classes
4. Use black for code formatting
5. Use isort for import sorting
