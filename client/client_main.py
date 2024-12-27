import asyncio
from client import VideoTranslationClient

async def start_and_get_status(client, job_id):
    """
    Start a translation job and get the status asynchronously.
    """
    print(f"Started job with ID: {job_id}")
    status = await client.async_get_status(job_id)
    print(f"Final status for job {job_id}: {status}")

async def main():
    client = VideoTranslationClient("http://localhost:7999")

    # List of jobs to be processed concurrently
    job_ids = []

    # Start normal translation jobs
    for _ in range(3):
        job_id = client.start_translation()
        if job_id:
            job_ids.append(job_id)
        else:
            print("Failed to start translation job.")

    # Special job ID for testing with exponential backoff
    special_job_id = "special-pending-job"
    print(f"Started special job with ID: {special_job_id}")
    job_ids.append(special_job_id)

    tasks = [start_and_get_status(client, job_id) for job_id in job_ids]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())