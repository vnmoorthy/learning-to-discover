"""Thread-safe pub/sub bus feeding the SSE endpoint (publishers are plain threads, subscribers asyncio queues)."""
import asyncio
import threading

_subs = []          # list of (loop, queue)
_lock = threading.Lock()


def subscribe():
    loop = asyncio.get_running_loop()
    qu = asyncio.Queue(maxsize=1000)
    with _lock:
        _subs.append((loop, qu))
    return qu


def unsubscribe(qu):
    with _lock:
        for s in list(_subs):
            if s[1] is qu:
                _subs.remove(s)


def _put(qu, item):
    try:
        qu.put_nowait(item)
    except asyncio.QueueFull:
        pass


def publish(event, data):
    with _lock:
        subs = list(_subs)
    for loop, qu in subs:
        try:
            loop.call_soon_threadsafe(_put, qu, (event, data))
        except RuntimeError:  # loop closed
            unsubscribe(qu)


def log(msg, level="info"):
    publish("log", {"level": level, "msg": msg})
    print(f"[ltd {level}] {msg}", flush=True)
