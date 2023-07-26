import argparse
import logging
from pathlib import Path

from playlist_ctl.config import Config
from playlist_ctl.defaults import default_config_path
from playlist_ctl.mpv_client import MpvClient
from playlist_ctl.rofi_client import RofiClient
from playlist_ctl.storage import Storage


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", metavar="URL", help="add new title")
    parser.add_argument(
        "-c",
        "--config",
        default=default_config_path(),
        metavar="PATH",
        type=Path,
        help="config file path (default: %(default)s)",
    )
    parser.add_argument(
        "-s",
        "--socket",
        default=Path("/tmp/mpv.sock"),
        metavar="PATH",
        help="socket file (default: %(default)s)",
    )
    return parser.parse_args()


def init_logger(level: int, file: Path) -> None:
    log = logging.getLogger()
    log.setLevel(level)
    fh = logging.FileHandler(file)
    fh.setFormatter(
        logging.Formatter(
            fmt="[%(asctime)s %(levelname)s] %(message)s (%(funcName)s:%(lineno)d)",
            datefmt="%H:%M:%S %d/%m/%y",
        )
    )
    log.addHandler(fh)


def main():
    args = parse_args()
    config = Config(config_file=args.config, socket_file=args.socket)
    if config.cache_dir.exists() and not config.cache_dir.is_dir():
        exit("%s is ivalid cache directory" % config.cache_dir)
    if not config.cache_dir.exists():
        config.cache_dir.mkdir(parents=True)
    if config.log_level > 0:
        init_logger(config.log_level, config.log_file)

    stor = Storage(config.storage_file)
    if err := stor.init_db():
        exit("can't create table: %s" % err)

    mpv = MpvClient(args.socket)
    if args.add:
        if err := mpv.append(args.add):
            exit(str(err))
        if err := stor.add_title(args.add):
            exit(str(err))
    else:
        RofiClient(stor, mpv).print_playlist()
