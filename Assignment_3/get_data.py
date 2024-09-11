import threading
import time
import requests
import json
import queue

file_path = 'posts.json'
url = "https://jsonplaceholder.typicode.com/posts/{post_index}"
POSTS_AMOUNT = 77

posts_queue = queue.Queue()
lock = threading.Lock()

def read_json():
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_json(data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def save_posts():
    posts_list = []
    while not posts_queue.empty():
        posts_list.append(posts_queue.get())

    write_json(posts_list)

def get_data(post_index):
    print(f"Request sent for post {post_index}")
    response = requests.get(url.format(post_index=post_index))
    if response.status_code == 200:
        data = response.json()
        posts_queue.put(data)
        print(f'Post {post_index} fetched successfully.')
    else:
        print(f'Post {post_index} fetching failed.')

def get_id(post):
    return post['id']

def sort_data():
    data = read_json()
    data = sorted(data, key=get_id)
    write_json(data)

def main():
    threads = []
    start_time = time.time()
    for post_index in range(1, POSTS_AMOUNT+1):
        thread = threading.Thread(target=get_data, args=(post_index,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    save_posts()
    end_time = time.time() - start_time

    print(f"Time spent for data fetching and saving {end_time:.2f} seconds")

    # Prioritized fast retrieval/saving of posts, sorting by IDs wasn't
    # required initially, so sorting is done afterward.
    sort_data()

if __name__ == '__main__':
    main()
