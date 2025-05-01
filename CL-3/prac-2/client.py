import Pyro4
import sys

def main():
    try:
        # Try to read the server URI
        try:
            with open("server_uri.txt", "r") as f:
                uri = f.read().strip()
        except FileNotFoundError:
            print("Error: server_uri.txt not found. Make sure the server is running.")
            sys.exit(1)

        # Connect to the server
        try:
            server = Pyro4.Proxy(uri)
        except Pyro4.errors.CommunicationError:
            print("Error: Could not connect to the server. Make sure the server is running.")
            sys.exit(1)

        # Get input from user
        str1 = input("Enter the first string: ")
        str2 = input("Enter the second string: ")

        # Call the remote method
        try:
            result = server.concatenate_strings(str1, str2)
            print("Concatenated Result:", result)
        except Pyro4.errors.CommunicationError:
            print("Error: Lost connection to the server.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()