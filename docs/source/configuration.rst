Configuration
=============

Environment Variables
-------------------

Configure BossKit using environment variables:

.. code-block:: bash

    export BOSSKIT_API_KEY="your_api_key"
    export BOSSKIT_MODEL="gpt-3.5-turbo"

Python Configuration
-------------------

Configure using Python:

.. code-block:: python

    from bosskit import BossKit

    bk = BossKit(
        api_key="your_api_key",
        default_model="gpt-3.5-turbo"
    )
