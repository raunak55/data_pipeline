import concurrent.futures
import time

def task(n):
    print(f"Task {n} starting...")
    time.sleep(2)
    print(f"Task {n} finished!")
    return n * 2

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit multiple tasks for execution
        futures = [executor.submit(task, i) for i in range(5)]
        
        # Wait for all tasks to complete and retrieve results
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    print("All tasks completed. Results:", results)
