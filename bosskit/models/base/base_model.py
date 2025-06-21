from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ModelMessage:
    role: str
    content: str
    name: Optional[str] = None

@dataclass
class ModelSettings:
    name: str
    edit_format: str = "whole"
    weak_model_name: Optional[str] = None
    use_repo_map: bool = False
    send_undo_reply: bool = False
    lazy: bool = False
    overeager: bool = False
    reminder: str = "user"
    examples_as_sys_msg: bool = False
    extra_params: Optional[Dict[str, Any]] = None
    cache_control: bool = False
    caches_by_default: bool = False
    use_system_prompt: bool = True
    use_temperature: Union[bool, float] = True
    streaming: bool = True
    editor_model_name: Optional[str] = None
    editor_edit_format: Optional[str] = None
    reasoning_tag: Optional[str] = None
    remove_reasoning: Optional[str] = None
    system_prompt_prefix: Optional[str] = None
    accepts_settings: Optional[list] = None

class BaseModel(ABC):
    def __init__(self, settings: ModelSettings):
        self.settings = settings
        self.verbose = False
        self.max_chat_history_tokens = 1024
        self.weak_model = None
        self.editor_model = None
        self.missing_keys = None
        self.keys_in_environment = None

    @abstractmethod
    def validate_environment(self) -> Dict[str, Any]:
        """Validate environment variables and return missing keys."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information."""
        pass

    @abstractmethod
    def send_completion(
        self,
        messages: List[ModelMessage],
        functions: Optional[List[Dict[str, Any]]] = None,
        stream: bool = False,
        temperature: Optional[float] = None
    ) -> Any:
        """Send completion request to the model."""
        pass

    def token_count(self, messages: List[ModelMessage]) -> int:
        """Calculate token count for messages."""
        raise NotImplementedError

    def token_count_for_image(self, image_path: Path) -> int:
        """Calculate token count for an image."""
        raise NotImplementedError
