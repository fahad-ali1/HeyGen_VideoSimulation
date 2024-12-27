import aiohttp
import asyncio
import requests
import logging

# Configurable retries and backoff exponential factor
RETRIES = 5
BACKOFF_FACTOR = 1

logging.basicConfig(
    level=logging.INFO,
    format="\n%(levelname)s: %(message)s")

class VideoTranslationClient:
    def __init__(self, base_url, max_retries=RETRIES, backoff_factor=BACKOFF_FACTOR):
        """
        Initializes the client with the server's URL, maximum retries, backoff factor.
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def start_translation(self):
        """
        Start a new video translation job. Gets the job ID from the server.

        Returns:
            str: Job ID if the job was successfully started, None otherwise.
        Raises:
            requests.exceptions.ConnectionError: If the client fails to connect to the server.
            Exception: For any other unexpected errors.
        """
        try:
            response = requests.post(f"{self.base_url}/start")
            response.raise_for_status()
            return response.json().get("job_id")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to start translation. \nERROR: {e}")
            return None

    async def async_get_status(self, job_id):
        """
        Asynchronously polls the server for the status of the video translation using the job ID.
        Uses exponential backoff to reduce server load effectively.

        Args:
            job_id (str): Unique identifier for the translation job.
        Returns:
            str: Final status of the job ("completed", "error", "pending", "server offline").
        Raises:
            aiohttp.ClientError: If the client fails to connect to the server asynchronously.
            Exception: For any other unexpected errors.
        """
        if job_id is None:
            logging.warning("No job ID provided.")
            return "No job ID provided."

        url = f"{self.base_url}/status/{job_id}"
        retries = 0
        logging.info("Please wait while we translate the video asynchronously...")
        async with aiohttp.ClientSession() as session:
            while retries < self.max_retries:
                try:
                    async with session.get(url) as response:
                        response.raise_for_status()
                        result = await response.json()
                        if result.get("result") in ["completed", "error"]:
                            return result.get("result")
                        else:
                            delay = self.backoff_factor * (2 ** retries)
                            logging.info(f"Async status: {result.get("result")}. Status check {retries + 1}. Waiting {delay} seconds before next status check.")
                            await asyncio.sleep(delay)
                            retries += 1
                except aiohttp.ClientError as e:
                    logging.error(f"Async error: {e}")
                    return "server offline"
            return "pending"