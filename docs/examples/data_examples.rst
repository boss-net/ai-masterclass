Data Processing Examples
======================

Basic Usage
-----------

.. code-block:: python

    from bosskit.utils.data import get_data_processor

    # Create data processor
    processor = get_data_processor()

    # Validate data
    schema = {
        "name": {"type": str, "required": True},
        "age": {"type": int, "required": True},
        "email": {"type": str, "required": True}
    }

    try:
        processor.validate_data({"name": "John", "age": 30}, schema)
    except ValidationError as e:
        print(f"Validation error: {str(e)}")

Data Transformation
------------------

.. code-block:: python

    from bosskit.utils.data import get_data_processor

    # Create data processor
    processor = get_data_processor()

    # Define transformation mapping
    mapping = {
        "full_name": "name",
        "years_old": lambda d: d.get("age", 0),
        "contact": {
            "email": "email",
            "phone": lambda d: d.get("phone", "N/A")
        }
    }

    # Transform data
    original_data = {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "phone": "123-456-7890"
    }

    transformed = processor.transform_data(original_data, mapping)
    print(transformed)

Data Filtering
-------------

.. code-block:: python

    from bosskit.utils.data import get_data_processor

    # Create data processor
    processor = get_data_processor()

    # Define filter conditions
    conditions = {
        "age": {"$gt": 25},
        "active": True,
        "role": {"$in": ["admin", "manager"]}
    }

    # Filter data
    users = [
        {"name": "Alice", "age": 30, "active": True, "role": "admin"},
        {"name": "Bob", "age": 22, "active": True, "role": "user"},
        {"name": "Charlie", "age": 35, "active": False, "role": "manager"},
        {"name": "David", "age": 40, "active": True, "role": "manager"}
    ]

    filtered = [u for u in users if processor.filter_data(u, conditions)]
    print(filtered)

Data Serialization
-----------------

.. code-block:: python

    from bosskit.utils.data import get_data_processor

    # Create data processor
    processor = get_data_processor()

    # Serialize to JSON
    data = {"name": "John", "age": 30}
    json_str = processor.serialize(data, format='json')

    # Serialize to YAML
    yaml_str = processor.serialize(data, format='yaml')

    # Serialize to pickle
    pickle_bytes = processor.serialize(data, format='pickle')

Data Merging
------------

.. code-block:: python

    from bosskit.utils.data import get_data_processor

    # Create data processor
    processor = get_data_processor()

    # Deep merge
    data1 = {"name": "John", "contact": {"email": "john@example.com"}}
    data2 = {"age": 30, "contact": {"phone": "123-456-7890"}}
    merged = processor.merge_data(data1, data2, strategy='deep')

    # Shallow merge
    data3 = {"name": "John", "age": 30}
    data4 = {"name": "Jane", "age": 25}
    merged_shallow = processor.merge_data(data3, data4, strategy='shallow')
