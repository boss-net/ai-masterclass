Configuration Guide
===================

Environment Variables
--------------------

BossKit uses several environment variables for configuration. These can be set in your shell or in a `.env` file.

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: BOSSKIT_API_KEY

   The API key for your model provider (e.g., OpenAI, Anthropic)

.. envvar:: BOSSKIT_MODEL

   The default model to use for AI operations

Optional Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: BOSSKIT_MAX_TOKENS

   Maximum number of tokens to use for model responses

.. envvar:: BOSSKIT_TEMPERATURE

   Temperature setting for model responses (0.0 to 1.0)

.. envvar:: BOSSKIT_TOP_P

   Top-p sampling parameter for model responses

Configuration File
-----------------

BossKit supports a configuration file at `~/.bosskit/config.yaml`. Here's an example configuration:

.. code-block:: yaml

    api:
      key: your-api-key-here
      provider: openai
      model: gpt-4

    settings:
      max_tokens: 2000
      temperature: 0.7
      top_p: 0.9

    system:
      memory_limit: 8GB
      cpu_limit: 4

Configuration Precedence
-----------------------

1. Command-line arguments
2. Environment variables
3. Configuration file
4. Default values

Custom Configuration
-------------------

You can create custom configurations for different environments:

.. code-block:: yaml

    development:
      api:
        key: dev-key
        model: gpt-3.5-turbo

    production:
      api:
        key: prod-key
        model: gpt-4
