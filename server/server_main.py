import uvicorn

if __name__ == "__main__":
    # Run the server using Uvicorn
    uvicorn.run("server:app", host="localhost", port=7999, reload=True)