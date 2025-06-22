import json
import logging
import time
import asyncio
from typing import Any, AsyncGenerator, Dict, Optional

import aiohttp  # type: ignore
import requests  # type: ignore

from .errors import APIError  # type: ignore


class NetworkClient:
    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30,
        retries: int = 3,
        backoff_factor: float = 1.0,
        logger: Optional[logging.Logger] = None,
    ):
        """Initialize the network client.

        Args:
            base_url: Base URL for API requests
            headers: Default headers
            timeout: Request timeout in seconds
            retries: Number of retries
            backoff_factor: Backoff factor for retries
            logger: Logger instance
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout
        self.retries = retries
        self.backoff_factor = backoff_factor
        self.logger = logger or logging.getLogger("bosskit.network")

    async def _retry_request(self, method: str, url: str, **kwargs) -> Any:
        """Make a request with retry logic.

        Args:
            method: HTTP method
            url: Request URL
            kwargs: Request parameters

        Returns:
            Response data

        Raises:
            APIError: If request fails after retries
        """
        for attempt in range(self.retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.request(method, url, timeout=self.timeout, **kwargs) as response:
                        if response.status >= 500:
                            raise APIError(f"Server error: {response.status}")
                        elif response.status == 429:
                            await asyncio.sleep(self.backoff_factor * (2**attempt))
                            continue
                        return await response.json()
            except asyncio.TimeoutError as exc:
                if attempt == self.retries - 1:
                    raise TimeoutError(f"Request timed out after {self.timeout}s") from exc
                await asyncio.sleep(self.backoff_factor * (2**attempt))
            except Exception as e:  # noqa: BLE001
                # Network errors can be varied and unpredictable
                if attempt == self.retries - 1:
                    raise APIError(f"Request failed: {str(e)}") from e
                await asyncio.sleep(self.backoff_factor * (2**attempt))

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """Make a GET request.

        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers

        Returns:
            Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        all_headers = {**self.headers, **(headers or {})}

        self.logger.info(f"GET request to {url}")
        return await self._retry_request("GET", url, params=params, headers=all_headers)

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        """Make a POST request.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Request headers

        Returns:
            Response data
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        all_headers = {**self.headers, **(headers or {})}

        self.logger.info(f"POST request to {url}")
        return await self._retry_request("POST", url, data=data, json=json_data, headers=all_headers)

    async def stream(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream data from an endpoint.

        Args:
            endpoint: API endpoint
            data: Form data
            json_data: JSON data
            headers: Request headers

        Yields:
            Response chunks
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        all_headers = {**self.headers, **(headers or {})}

        self.logger.info(f"Streaming from {url}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, json=json_data, headers=all_headers, timeout=self.timeout) as response:
                async for chunk in response.content:
                    if chunk:
                        yield json.loads(chunk.decode())

    @staticmethod
    async def download_file(url: str, output_path: str, chunk_size: int = 1024) -> None:
        """Download a file asynchronously.

        Args:
            url: File URL
            output_path: Output file path
            chunk_size: Chunk size in bytes
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(output_path, "wb") as f:
                    while True:
                        chunk = await response.content.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)


def sync_network_client(
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    retries: int = 3,
    backoff_factor: float = 1.0,
    logger: Optional[logging.Logger] = None,
) -> Any:
    """Create a synchronous network client.

    Args:
        base_url: Base URL for API requests
        headers: Default headers
        timeout: Request timeout in seconds
        retries: Number of retries
        backoff_factor: Backoff factor for retries
        logger: Logger instance

    Returns:
        Network client instance
    """

    class SyncNetworkClient:
        def __init__(self):
            self.session = requests.Session()
            self.base_url = base_url.rstrip("/")
            self.headers = headers or {}
            self.timeout = timeout
            self.retries = retries
            self.backoff_factor = backoff_factor
            self.logger = logger or logging.getLogger("bosskit.network.sync")

        def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None):
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            return self._retry_request("GET", url, params=params)

        def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None):
            url = f"{self.base_url}/{endpoint.lstrip('/')}"
            return self._retry_request("POST", url, json=data)

        def _retry_request(self, method: str, url: str, **kwargs) -> Any:
            for attempt in range(self.retries):
                try:
                    response = self.session.request(method, url, timeout=self.timeout, **kwargs)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.Timeout:
                    if attempt == self.retries - 1:
                        raise TimeoutError(f"Request timed out after {self.timeout}s")
                    time.sleep(self.backoff_factor * (2**attempt))
                except Exception as e:  # noqa: BLE001
                    # Network errors can be varied and unpredictable
                    if attempt == self.retries - 1:
                        raise APIError(f"Request failed: {str(e)}") from e
                    time.sleep(self.backoff_factor * (2**attempt))

    return SyncNetworkClient()
