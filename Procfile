# Define the process type for running the app
# - web: Indicates this is a web process (e.g., for Heroku)
# - uvicorn: Runs the FastAPI app with specified host and port
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app # from trackFinder