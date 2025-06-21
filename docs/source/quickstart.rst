Quickstart
==========

Basic Usage
-----------

Initialize BossKit:

.. code-block:: python

    from bosskit import BossKit

    bk = BossKit()

Use a model:

.. code-block:: python

    response = bk.model("gpt-3.5-turbo").chat("Hello, how are you?")
    print(f"Model response: {response}")

Caching:
--------

Enable caching:

.. code-block:: python

    bk.enable_caching()

    # Subsequent requests will be cached
    response = bk.model("gpt-3.5-turbo").chat("Hello again!")
