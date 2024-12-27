import asyncio
from client import VideoTranslationClient

async def main():
    client = VideoTranslationClient("http://localhost:7999")
    
    # Normal job ID
    job_id = client.start_translation()
    if job_id:
        print(f"Started job with ID: {job_id}")
        status = await client.async_get_status(job_id)
        print(f"\nFinal status: {status}")

    # Special job ID for testing exponential backoff
    # special_job_id = "special-pending-job"
    # print(f"Started job with ID: {special_job_id}")
    # status = await client.async_get_status(special_job_id)
    # print(f"\nFinal status: {status}")

if __name__ == "__main__":
    asyncio.run(main())