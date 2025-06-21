Network Examples
===============

Basic Usage
-----------

.. code-block:: python

    from bosskit.utils.network import NetworkClient

    # Create a network client
    client = NetworkClient(
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer your-token"}
    )

    # Make a GET request
    response = await client.get("/users")
    print(response)

Streaming Example
----------------

.. code-block:: python

    from bosskit.utils.network import NetworkClient

    # Create a network client
    client = NetworkClient(
        base_url="https://api.example.com",
        headers={"Authorization": "Bearer your-token"}
    )

    # Stream data
    async for chunk in client.stream("/events"):
        print(chunk)

Configuration Example
--------------------

.. code-block:: python

    from bosskit.utils.config import get_config_manager

    # Create config manager
    config = get_config_manager()

    # Set configuration values
    config.set("api_key", "your-api-key")
    config.set("model", "gpt-4")

    # Get configuration value
    api_key = config.get("api_key")

    # Load from file
    config.load_from_file("config.yaml")

    # Validate configuration
    schema = {
        "api_key": {"type": str, "required": True},
        "model": {"type": str, "required": True}
    }
    is_valid = config.validate(schema)
