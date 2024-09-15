# FetchData App

## Description

The `FetchData` application is designed to asynchronously fetch and store posts from a provided API. The number of posts can be configured by the user, and the app ensures the data is saved in a local `posts.json` file. The app is capable of fetching up to 100 posts in parallel using Python's `asyncio` and `aiohttp` libraries.

## Features

- Fetch posts asynchronously from the provided API.
- Save fetched data into a `posts.json` file.
- Automatically handle a maximum of 100 posts.
- Optional method to sort the saved data by the `id` field.
- Thread-safe saving of posts data using `asyncio.Lock`.

## Requirements

- Python 3.8+
- `aiohttp` library for handling asynchronous HTTP requests.

**Note**: `asyncio` is part of the Python standard library, so no additional installation is required for it.

You can install the required `aiohttp` library using:
```bash
pip install aiohttp

