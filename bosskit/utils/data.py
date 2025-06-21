import json
import logging
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, TypeVar, Union

import yaml

from .errors import ValidationError
from .logging_utils import setup_logger

T = TypeVar('T')

class DataProcessor:
    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize the data processor.

        Args:
            logger: Logger instance
        """
        self.logger = logger or setup_logger('bosskit.data')

    def validate_data(
        self,
        data: Any,
        schema: Dict[str, Any],
        path: str = ''
    ) -> bool:
        """Validate data against a schema.

        Args:
            data: Data to validate
            schema: Validation schema
            path: Path for error reporting

        Returns:
            True if valid, False otherwise

        Raises:
            ValidationError: If validation fails
        """
        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise ValidationError(f"{path}: Expected dict, got {type(data).__name__}")

            for key, value_schema in schema.items():
                if key not in data:
                    if value_schema.get('required', False):
                        raise ValidationError(f"{path}: Missing required field '{key}'")
                    continue

                self.validate_data(data[key], value_schema, f"{path}.{key}")
        elif isinstance(schema, list):
            if not isinstance(data, list):
                raise ValidationError(f"{path}: Expected list, got {type(data).__name__}")

            for item in data:
                self.validate_data(item, schema[0], path)
        else:
            if not isinstance(data, schema):
                raise ValidationError(
                    f"{path}: Expected {schema.__name__}, got {type(data).__name__}"
                )
        return True

    def serialize(
        self,
        data: Any,
        format: str = 'json',
        path: Optional[Path] = None
    ) -> Union[str, bytes]:
        """Serialize data to a format.

        Args:
            data: Data to serialize
            format: Output format ('json', 'yaml', 'pickle')
            path: Optional output path

        Returns:
            Serialized data

        Raises:
            ValueError: If format is not supported
        """
        if format == 'json':
            content = json.dumps(data, indent=2)
        elif format == 'yaml':
            content = yaml.dump(data)
        elif format == 'pickle':
            content = pickle.dumps(data)
        else:
            raise ValueError(f"Unsupported format: {format}")

        if path:
            with open(path, 'wb' if format == 'pickle' else 'w') as f:
                f.write(content)

        return content

    def deserialize(
        self,
        data: Union[str, bytes],
        format: str = 'json',
        path: Optional[Path] = None
    ) -> Any:
        """Deserialize data from a format.

        Args:
            data: Data to deserialize
            format: Input format ('json', 'yaml', 'pickle')
            path: Optional input path

        Returns:
            Deserialized data

        Raises:
            ValueError: If format is not supported
        """
        if format == 'json':
            if path:
                with open(path, 'r') as f:
                    return json.load(f)
            return json.loads(data)

        elif format == 'yaml':
            if path:
                with open(path, 'r') as f:
                    return yaml.safe_load(f)
            return yaml.safe_load(data)

        elif format == 'pickle':
            if path:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            return pickle.loads(data)

        raise ValueError(f"Unsupported format: {format}")

    def transform_data(
        self,
        data: Any,
        mapping: Dict[str, Any],
        path: str = ''
    ) -> Any:
        """Transform data using a mapping.

        Args:
            data: Data to transform
            mapping: Transformation mapping
            path: Path for error reporting

        Returns:
            Transformed data

        Raises:
            ValueError: If transformation fails
        """
        if isinstance(mapping, dict):
            if not isinstance(data, dict):
                raise ValueError(f"{path}: Expected dict, got {type(data).__name__}")

            result = {}
            for key, transform in mapping.items():
                if isinstance(transform, str):
                    result[key] = data.get(transform)
                elif callable(transform):
                    result[key] = transform(data)
                else:
                    result[key] = self.transform_data(
                        data.get(key),
                        transform,
                        f"{path}.{key}"
                    )
            return result

        raise ValueError(f"Invalid mapping at {path}")

    def merge_data(
        self,
        *data: Any,
        strategy: str = 'deep'
    ) -> Any:
        """Merge multiple data structures.

        Args:
            *data: Data to merge
            strategy: Merge strategy ('deep', 'shallow')

        Returns:
            Merged data
        """
        if not data:
            return None

        result = data[0]
        for d in data[1:]:
            if strategy == 'deep':
                result = self._deep_merge(result, d)
            else:
                result = self._shallow_merge(result, d)
        return result

    def _deep_merge(self, a: Any, b: Any) -> Any:
        """Deep merge two data structures."""
        if isinstance(a, dict) and isinstance(b, dict):
            result = a.copy()
            for key, value in b.items():
                if key in a:
                    result[key] = self._deep_merge(a[key], value)
                else:
                    result[key] = value
            return result

        if isinstance(a, list) and isinstance(b, list):
            return a + b

        return b

    def _shallow_merge(self, a: Any, b: Any) -> Any:
        """Shallow merge two data structures."""
        if isinstance(a, dict) and isinstance(b, dict):
            return {**a, **b}
        return b

    def filter_data(
        self,
        data: Any,
        conditions: Dict[str, Any],
        path: str = ''
    ) -> Any:
        """Filter data based on conditions.

        Args:
            data: Data to filter
            conditions: Filter conditions
            path: Path for error reporting

        Returns:
            Filtered data
        """
        if isinstance(conditions, dict):
            if not isinstance(data, dict):
                return None

            if all(
                self._matches_condition(data.get(key), value)
                for key, value in conditions.items()
            ):
                return data
            return None

        raise ValueError(f"Invalid conditions at {path}")

    def _matches_condition(self, value: Any, condition: Any) -> bool:
        """Check if a value matches a condition."""
        if isinstance(condition, dict):
            if '$eq' in condition:
                return value == condition['$eq']
            if '$ne' in condition:
                return value != condition['$ne']
            if '$gt' in condition:
                return value > condition['$gt']
            if '$lt' in condition:
                return value < condition['$lt']
            if '$gte' in condition:
                return value >= condition['$gte']
            if '$lte' in condition:
                return value <= condition['$lte']
            if '$in' in condition:
                return value in condition['$in']
            if '$nin' in condition:
                return value not in condition['$nin']
        return value == condition

def get_data_processor(logger: Optional[logging.Logger] = None) -> DataProcessor:
    """Get a data processor instance.

    Args:
        logger: Logger instance

    Returns:
        DataProcessor instance
    """
    return DataProcessor(logger=logger)
