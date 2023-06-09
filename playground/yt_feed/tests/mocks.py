from functools import lru_cache
from typing import List
from models import Entry, Channel

entry_fmt = """
\t<entry>
  <yt:videoId>{id}</yt:videoId>
  <title>{title}</title>
  <updated>{updated}</updated>
</entry>
"""
feed_fmt = """
<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns:yt="http://www.youtube.com/xml/schemas/2015" xmlns:media="http://search.yahoo.com/mrss/" xmlns="http://www.w3.org/2005/Atom">
 <title>{channel_title}</title>
 <link rel="alternate" href="https://www.youtube.com/channel/{channel_id}"/>
 {entries}
</feed>
"""


@lru_cache(maxsize=1)
def sample_entries() -> List[Entry]:
    return [
        Entry(
            id=f"video_id_{n:02d}",
            title=f"Video #{n}",
            updated=f"2023-01-{n:02d}T00:00:00+00:00",
        )
        for n in range(1, 4)
    ]


@lru_cache(maxsize=1)
def sample_channel() -> Channel:
    return Channel(
        channel_id="sample_channel_id1234567",
        title="Sample Channel",
        entries=sample_entries(),
    )


def raw_feed() -> str:
    channel = sample_channel()
    return feed_fmt.format(
        channel_title=channel.title,
        channel_id=channel.channel_id,
        entries="".join(
            entry_fmt.format(id=e.id, title=e.title, updated=e.updated).strip()
            for e in channel.entries
        ),
    ).strip()
