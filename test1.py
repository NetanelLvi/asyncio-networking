import asyncio
import time 

async def fetch_data(delay, id):
    print("fetching data", id)
    await asyncio.sleep(delay, id)
    print("data fetched", id)
    return {'data': "some data.",
            'id': id}

async def main():
    print('start of main coroutine')
    task1 = fetch_data(2,1)
    task2 = fetch_data(2,2)
    print("end of main coroutine")

    result1 = await task1
    print(f'receive result {result1}')
    
    result2 = await task2
    print(f'receive result {result2}')    
    

if __name__=='__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()

    print(f' took {(end_time - start_time):.2f} sec')