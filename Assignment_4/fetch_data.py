import time
import aiohttp
import asyncio
import json
from pathlib import Path

class FetchData:
    def __init__(self, posts_count:int = 77, url:str = ''):
        if posts_count <= 0:
            raise ValueError("Posts count should be a positive integer.")
        elif posts_count > 100:
            print("Posts amount reduced to 100.")
        self.url = url
        self.script_dir = Path(__file__).parent
        self.file_path = self.script_dir / 'posts.json'
        self.__posts_count = min(posts_count, 100)
        self.__lock = asyncio.Lock()
        self.__posts = []
        
    def fetch(self):
        asyncio.run(self.__create_tasks())
        
    async def __create_tasks(self):
        tasks = [self.__fetch_api_data(post_id=post_id) for post_id in range(1, self.__posts_count + 1)]
        await asyncio.gather(*tasks)
        
    async def __fetch_api_data(self, post_id:int):
        print(f"Requesting data for post_id: {post_id}")
        async with aiohttp.request('GET', self.url.format(post_id=post_id)) as response:
            if response.status != 200:
                raise ConnectionError("Failed to fetch data from the API.")
            post_data = await response.json()
            async with self.__lock:
                self.__posts.append(post_data)
                self.__save_data(self.__posts)
                print(f"Data for post_id: {post_id} saved.")
                
    def __save_data(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)

    # Optional method to sort the data by 'id' field
    def sort_data(self):
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            data.sort(key=lambda x: x['id'])
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()


if __name__ == '__main__':
    start_time = time.time()
    api_url = "https://jsonplaceholder.typicode.com/posts/{post_id}"
    fetch_data = FetchData(url=api_url)
    fetch_data.fetch()
    elapsed_time = time.time() - start_time
    print(f'Elapsed time: {elapsed_time:.2f} seconds')
    # Not required for the assignment
    fetch_data.sort_data()
    