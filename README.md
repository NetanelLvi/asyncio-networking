# asyncio-networking

## Fundamentals of Python `asyncio==3.4.3`

`Asyncio`: stands for Asynchronous Input Output

Python's `asyncio` is a library for writing concurrent code using asynchronous I/O. It's particularly useful for I/O-bound operations (e.g., networking, database queries) where tasks spend a lot of time waiting for data to become available. Unlike traditional threading or multiprocessing, `asyncio` uses a single-threaded, cooperative multitasking model based on an event loop.

---

## **Common Keywords, Their Uses, and Meaning**

1. **`async`**:
   - **Use**: Marks a function as a coroutine, allowing it to use `await`.
   - **Meaning**: A coroutine is a function that can pause and resume execution to perform non-blocking tasks.
   - **Example**:

   ``` py
     async def fetch_data():
         print("Fetching data...")
         await asyncio.sleep(2)  # Simulates a delay
         print("Data fetched.")
   ```

2. **`await`**:
   - **Use**: Pauses execution of the coroutine until the awaited task completes.
   - **Meaning**: Suspends the current coroutine and allows the event loop to perform other tasks.
   - **Example**:

   ```py
         await asyncio.sleep(1)
   ```

3. **`asyncio.run()`**:
   - **Use**: Runs the top-level entry point of an `asyncio` program.
   - **Meaning**: Starts the event loop and runs the specified coroutine.
   - **Example**:

   ```py
     import asyncio
     asyncio.run(fetch_data())
   ```

4. **`asyncio.create_task()`**:
   - **Use**: Schedules a coroutine to run concurrently as a task.
   - **Meaning**: Allows multiple coroutines to execute concurrently.
   - **Example**:

     ```python
     import asyncio
     task = asyncio.create_task(fetch_data())
     ```

5. **`asyncio.sleep()`**:
   - **Use**: Pauses execution of a coroutine for a specified time.
   - **Meaning**: Non-blocking delay used for simulating I/O or timing operations.
   - **Example**:

   ```python
     await asyncio.sleep(2)
     ```

6. **`asyncio.gather()`**:
   - **Use**: Runs multiple coroutines concurrently and waits for all of them to finish.
   - **Meaning**: Aggregates results from concurrent coroutines.
   - **Example**:

   ```python
         import asyncio
         results = await asyncio.gather(fetch_data(), fetch_data())
   ```

---

### **Theory and Mechanics of `asyncio`**

#### 1. **How It Works**

- `asyncio` uses an **event loop**, which acts as a central controller:
     1. Tasks are scheduled on the event loop.
     2. When a coroutine performs an `await`, the event loop pauses it and runs other tasks.
     3. Once the awaited task completes, the paused coroutine resumes execution.
- It achieves concurrency without threads by cooperatively switching between tasks.

#### 2. **Implementing Code Using `asyncio`**

- Structure:
     1. Define asynchronous functions (`async def`).
     2. Use `await` for non-blocking I/O operations.
     3. Schedule coroutines using `asyncio.run()` or `asyncio.create_task()`.
- Example:

   ```python
      import asyncio

      async def fetch_data(task_name, delay):
         print(f"{task_name}: Fetching data...")
         await asyncio.sleep(delay)  # Simulate I/O delay
         print(f"{task_name}: Data fetched.")

     async def main():
         # Run two tasks concurrently
         await asyncio.gather(
             fetch_data("Task 1", 2),
             fetch_data("Task 2", 3)
         )

     asyncio.run(main())
   ```

#### 3. **Advantages**

- High performance for I/O-bound tasks.
- Low memory usage (single-threaded).
- Simplifies asynchronous programming with `await`.

#### 4. **Limitations**

- Not suitable for CPU-bound tasks.
- Runs on a single thread (no parallelism for CPU-heavy computations).

---

### **Comparison: Multithreading, Multiprocessing, and `asyncio`**

| **Feature**            | **Asyncio**                  | **Multithreading**               | **Multiprocessing**            |
|-------------------------|-----------------------------|-----------------------------------|---------------------------------|
| **Purpose**             | Asynchronous I/O-bound tasks| Concurrency for I/O-bound tasks   | Parallelism for CPU-bound tasks |
| **Concurrency Model**   | Cooperative multitasking    | Preemptive multitasking           | Parallel processes              |
| **Threads/Processes**   | Single thread               | Multiple threads                  | Multiple processes              |
| **Parallelism**         | No                          | Limited (GIL-bound)               | Yes                             |
| **Use of GIL**          | Doesn't affect GIL          | Affected by GIL                   | Not affected by GIL             |
| **Memory Usage**        | Low                         | Moderate                          | High                            |
| **Use Cases**           | High-performance I/O, networking | Networking, GUIs                 | Machine learning, heavy computation |
| **Implementation**      | Coroutines                  | Threads                           | Processes                       |
| **Example Use**         | Web servers                 | Web scraping                      | Data processing pipelines       |

---

### **Choosing the Right Tool**

1. **When to Use `asyncio`**:
   - Handling a large number of network connections (e.g., chat servers, HTTP clients).
   - Tasks are mostly waiting on external resources (I/O).

2. **When to Use Multithreading**:
   - GUIs or applications where threads need to interact with the main thread.
   - When dealing with blocking I/O in libraries that don't support async.

3. **When to Use Multiprocessing**:
   - CPU-intensive tasks (e.g., video encoding, numerical simulations).
   - Scenarios requiring parallelism across multiple cores.

By understanding these distinctions and the power of `asyncio`, you can write efficient and scalable Python applications tailored to your workload.

#### GIL

The GIL (Global Interpreter Lock) is a mutex (mutual exclusion lock) used in CPython, the most common implementation of Python. It ensures that only one thread executes Python bytecode at a time, even on multi-core systems.
