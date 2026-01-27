from functions.get_files_info import get_files_info


def main():
    # Current directory
    print("Result for current directory:")
    result = get_files_info("calculator", ".")
    print(result)
    print()

    # pkg directory
    print("Result for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(result)
    print()

    # /bin directory (outside allowed)
    print("Result for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)
    print()

    # ../ directory (outside allowed)
    print("Result for '../' directory:")
    result = get_files_info("calculator", "../")
    print(result)


if __name__ == "__main__":
    main()
