import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="PROG", add_help=False)
    foo_group = parser.add_argument_group("foo", "foo group description")
    foo_group.add_argument("-a", help="a help")
    foo_group.add_argument("-b", help="b help")
    bar_group = parser.add_argument_group("bar", "bar group description")
    bar_group.add_argument("-c", help="c help")
    bar_group.add_argument("-d", help="d help")
    parser.print_help()
