from functions import start

def print_banner():
    banner = """
    *******************************
    *                             *
    *         WELCOME TO          *
    *       DATA IMPORT TOOL      *
    *                             *
    *******************************
    """
    print(banner)


def get_input():
    while True:
        try:
            print("How many rows do you want to import? ")
            qtd_rows = int(input("Qtd of rows: "))
            if qtd_rows > 0:
                return qtd_rows
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    print_banner()
    qtd_rows = get_input()
    start(qty=qtd_rows)  # Assuming start(qtd_rows) is already implemented


if __name__ == "__main__":
    main()
