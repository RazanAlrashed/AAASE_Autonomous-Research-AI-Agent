import time

def retry(func, retries=3, delay=5):

    for attempt in range(retries):

        try:

            return func()

        except Exception as e:

            print(f"Retry {attempt+1}/{retries}")

            if attempt == retries - 1:
                raise

            time.sleep(delay)