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

TEST_ENTRIES = [
    Entry(
        id=f"video_id_{n:02d}",
        title=f"Video #{n}",
        updated=f"2023-01-{n:02d}T00:00:00+00:00",
    )
    for n in range(1, 4)
]

TEST_FEED = Channel(
    channel_id="sample_channel_id1234567",
    title="Sample Channel",
    entries=TEST_ENTRIES,
)


def raw_test_feed() -> str:
    return feed_fmt.format(
        channel_title=TEST_FEED.title,
        channel_id=TEST_FEED.channel_id,
        entries="".join(
            entry_fmt.format(id=e.id, title=e.title, updated=e.updated).strip()
            for e in TEST_ENTRIES
        ),
    ).strip()
