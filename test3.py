import asyncio
import time 

async def fetch_data(id, sleep_time):
    print(f"coroutine {id} starting to fetch data")
    await asyncio.sleep(id, sleep_time)

    return {'id': id, "data": f"sample data from coroutine{id}."}

async def main():
    print('start of main coroutine')
    task1 = asyncio.create_task(fetch_data(1,2))
    task2 = asyncio.create_task(fetch_data(2,3))
    print("end of main coroutine")

    result1 = await task1
    print(f'receive result {result1}\n')
    result2 = await task2
    print(f'receive result {result2}\n')
    
    task3 = asyncio.create_task(fetch_data(3,1))
    result3 = await task3
    print(f'receive result {result3}\n')  
    # print(result1, result2, result3)
    

if __name__=='__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()

    print(f' took {(end_time - start_time):.2f} sec')
    