import sys

from .updater import update_app


def calculate_rectangle():
    print("Joph Rectangle Calculator")
    print("-------------------------")

    try:
        length = float(input("Enter the length: "))
        width = float(input("Enter the width: "))

        area = length * width

        print(f"Area: {area}")

    except ValueError:
        print("Error: please enter numbers only.")


def main():
    if len(sys.argv) == 1:
        calculate_rectangle()
        return

    command = sys.argv[1]

    if command == "update":
        update_app()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()