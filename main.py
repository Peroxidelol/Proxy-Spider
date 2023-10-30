import aiohttp
from aiofiles import open as aio_open
from colorama import Fore
import os
from pystyle import *
import asyncio 

proxy_list_file = 'proxy_list.txt'  
working_proxies_file = 'working_proxies.txt'  

async def check_proxy(proxy, url, session, semaphore):
    try:
        async with semaphore:
            async with session.get(url, proxy=f'http://{proxy}', timeout=2) as response:
                if response.status == 200:
                    print(f"Proxy {Fore.GREEN}{proxy}{Fore.RESET} is working")

                    with open(working_proxies_file, 'a') as output_file:
                        output_file.write(proxy + '\n')
                else:
                    print(f"Proxy {Fore.RED}{proxy}{Fore.RESET} isn't working")
    except aiohttp.ClientConnectorError:
        pass
    except asyncio.TimeoutError:
        print(f"Proxy {Fore.RED}{proxy}{Fore.RESET} isn't working")
    except aiohttp.ServerDisconnectedError:
        print(f"Proxy {Fore.RED}{proxy}{Fore.RESET} isn't working")
    except Exception as e:
        print(f"Proxy {Fore.YELLOW}{proxy}{Fore.RESET} encountered an unexpected error: {e}")

async def check_proxies_in_batches(proxy_list, url, session, batch_size):
    semaphore = asyncio.Semaphore(batch_size)
    tasks = []

    for proxy in proxy_list:
        task = check_proxy(proxy, url, session, semaphore)
        tasks.append(task)

    await asyncio.gather(*tasks)

async def main():
    os.system("cls")
    os.system("title Proxy Spider")
    ascii = f"""

                                                                      
 _____ _____ _____ __ __ __ __    _____ _____ _____ ____  _____ _____ 
|  _  | __  |     |  |  |  |  |  |   __|  _  |_   _|    \|   __| __  |
|   __|    -|  |  |-   -|_   _|  |__   |   __|_| |_ | |  |   __|    -|
|__|  |__|__|_____|__|__| |_|    |_____|__|  |_____|____/|_____|__|__|
                                                                      

    """
    print(Colorate.Horizontal(Colors.blue_to_cyan, Center.XCenter(ascii)))
    url = 'http://google.com'  
    batch_size = 20  

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with aio_open(proxy_list_file, mode='r') as file:
            proxy_list = (await file.read()).splitlines()

        await check_proxies_in_batches(proxy_list, url, session, batch_size)

if __name__ == '__main__':
    asyncio.run(main())
