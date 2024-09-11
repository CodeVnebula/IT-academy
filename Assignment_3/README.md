# Post Fetcher

## Description

This Python script fetches posts from the JSONPlaceholder API and saves them to a JSON file. It uses threading to fetch data concurrently, enhancing performance. After fetching, the script sorts the posts by their ID before saving them to ensure they are ordered correctly.

## Features

- Fetches posts from [JSONPlaceholder API](https://jsonplaceholder.typicode.com/posts)
- Uses threading to fetch multiple posts concurrently
- Saves the fetched posts to a JSON file
- Sorts posts by ID before saving to ensure proper order

## Modules Used

- **`threading`**: Enables concurrent execution of multiple threads to fetch posts in parallel.
- **`time`**: Measures the duration of the data fetching and saving process.
- **`requests`**: Handles HTTP requests to fetch posts from the API.
- **`json`**: Manages JSON data for reading from and writing to the file.
- **`queue`**: Provides a thread-safe queue to manage the posts fetched by different threads.


## Requirements

- Python 3.x
- `requests` library

## Usage

1. Install the required libraries:
    ```bash
    pip install requests
    ```

2. Run the script:
    ```bash
    python get_data.py
    ```

## File Details

- **posts.json**: The JSON file where the fetched posts are saved. It contains posts sorted by their ID.

## Notes

- The script uses a queue to manage and save posts efficiently.
- Sorting is performed after all posts are fetched and saved.

