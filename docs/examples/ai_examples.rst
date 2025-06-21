AI Examples
==========

Chat Completion
--------------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Basic chat completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]

    response = await processor.chat_completion(messages)
    print(response.choices[0].message.content)

Stream Chat Completion
---------------------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Stream chat completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing."}
    ]

    async for chunk in processor.stream_chat_completion(messages):
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)

Function Calling
---------------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Define functions
    functions = [
        {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        }
    ]

    # Function calling
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like in New York?"}
    ]

    response = await processor.function_calling(messages, functions)
    print(response)

Embeddings
----------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Generate embeddings
    texts = [
        "The cat sat on the mat.",
        "The dog chased the cat."
    ]

    embeddings = await processor.embeddings(texts)
    print(embeddings)

Image Generation
---------------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Generate images
    prompt = "A beautiful sunset over mountains"
    images = await processor.image_generation(
        prompt,
        n=2,
        size="1024x1024"
    )
    print(images)

Audio Transcription
------------------

.. code-block:: python

    from bosskit.utils.ai import get_ai_processor

    # Create AI processor
    processor = get_ai_processor()

    # Transcribe audio
    text = await processor.audio_transcription("audio.mp3")
    print(text)
