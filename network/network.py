import time
import asyncio
import urllib3
import httpx
import aiohttp
import os
import csv

URLS = [
    "https://nbg1-speed.hetzner.com/100MB.bin",
    "https://fsn1-speed.hetzner.com/100MB.bin",
    "https://hel1-speed.hetzner.com/100MB.bin",
]

SIZE = 100
RUNS = 1
results = []

def download_urllib3(url):
    http = urllib3.PoolManager()
    r = http.request("GET", url, preload_content=False)
    for _ in r.stream(8192):
        pass
    r.release_conn()

def download_httpx_sync(url):
    with httpx.Client() as client:
        with client.stream("GET", url) as r:
            for _ in r.iter_bytes():
                pass

async def download_httpx_async(url):
    async with httpx.AsyncClient() as client:
        async with client.stream("GET", url) as r:
            async for _ in r.aiter_bytes():
                pass

async def download_aiohttp(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            while await r.content.read(8192):
                pass

def run_sync_test(name, func, url):
    for _ in range(RUNS):
        start = time.perf_counter()
        func(url)
        elapsed = time.perf_counter() - start
    print_stats(name, url, elapsed)

async def run_async_test(name, coro_func, url):
    for _ in range(RUNS):
        start = time.perf_counter()
        await coro_func(url)
        elapsed = time.perf_counter() - start
    print_stats(name, url, elapsed)

def print_stats(lib_name, url, elapsed):
    endpoint = url.split('//')[1].split('/')[0]
    speed = SIZE / elapsed if elapsed > 0 else 0
    print(f"{lib_name:10s} | {endpoint:15s} | time: {elapsed:.5f}s | speed: {speed:.2f}MB/s")
    results.append({
        "Library": lib_name,
        "Endpoint": endpoint,
        "Time": f"{elapsed:.5f}",
        "Speed (MB/s)": f"{speed:.2f}"
    })

def get_next_filename(prefix="network", ext=".csv"):
    i = 1
    while os.path.exists(f"{prefix}{i}{ext}"):
        i += 1
    return f"{prefix}{i}{ext}"

async def main():
    for url in URLS:
        print(f"\nTesting endpoint: {url}")
        run_sync_test("urllib3", download_urllib3, url)
        run_sync_test("httpx-sync", download_httpx_sync, url)
        await run_async_test("httpx-async", download_httpx_async, url)
        await run_async_test("aiohttp", download_aiohttp, url)
    filename = get_next_filename()
    with open(filename, "w", newline="") as csvfile:
        fieldnames = ["Library", "Endpoint", "Time", "Speed (MB/s)"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print(f"\nResults saved in {filename}")

if __name__ == "__main__":
    asyncio.run(main())
