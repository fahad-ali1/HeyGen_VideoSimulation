# HeyGen Video Simulation
HeyGen Video Simulation is a simple FastAPI application that simulates video translation jobs that result in either completion or an error. The server provides endpoints to start a translation job and check its status. The client sends periodic get requests (with exponential back off factors) to check the status of the simulated video translation.

Features
---------
- Start Translation: Initiates a simulated video translation job. The delay can be configured in the server.py file.
- Check Status: Retrieves the status of a translation job.
- Testing: Tests the various features of this application with PyTest.

Requirements
-------------
Listed in requirements.txt

Installation
-------------
1. Clone the Repository:
   ```bash
   git clone https://github.com/fahad-ali1/HeyGen_VideoSimulation
   cd HeyGen_VideoSimulation
   ```

3. Create a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

5. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

Running the server
------------------------
1. Start the FastAPI Server (Note: Once live, any changes in the configurable portion of the code are hot reloaded):
   ```bash
   python3 server/server_main.py
   ```

Usage Overview
--------------

1. **Simulating a Video Translation Job**  
   To simulate a translation job (configurable):  
   - Send a POST request to `/start` to initiate a job and generate a unique job UUID.

2. **Checking Job Status**  
   To check the status of a job using its UUID:  
   - Send a GET request to `/status/{job_id}`. The status remains "pending" as long as the configurable duration as defined above.

3. **Running Concurrent Jobs**  
   When you run `client_main.py`, multiple translation jobs are processed concurrently (default: four jobs unless configured otherwise).  
   - One job (UUID: special-pending-job) is designed to always remain in a "pending" status to demonstrate the client’s exponential backoff strategy.  
   - The client avoids spamming the server with excessive GET requests and retries up to the maximum number of configurable retries with an exponential backoff (see below for configuration options).

### Example: Running the Simulation  
Ensure the server is running (e.g., `python3 server/server_main.py`) before executing the client. Run the client as follows:  
```bash
python3 client/client_main.py
```

Configurable Values
-------------------
Currently, dotenv is not implemented, but you can adjust the following values directly in the respective files:

1. **Simulation Delay for FastAPI Server**
   - **File:** `server.py` 
   - **Variable:** `DELAY`
   - **Default:** `5` (seconds)

2. **Retry Configurations**
   - **File:** `client.py`
   - **Variables:**
     - `RETRIES`: Number of retries for checking the status (default: `5`).
     - `BACKOFF_FACTOR`: Exponential backoff factor for status GET requests (default: `1`).

Note:
Once dotenv is implemented, these values can be moved to a `.env` file for easier configuration and management.

Running Tests
--------------
- While in the root directory, run this command:
   ```bash
   pytest -s tests/integration_test.py
   ```
