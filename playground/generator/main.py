from select_data import get_data


def main():
    while True:
        try:
            input("\nperform get_data\n")
        except KeyboardInterrupt:
            break
        else:
            print(get_data())


if __name__ == "__main__":
    main()
