import xmlrpc.client

def get_factorial():
    try:
        with xmlrpc.client.ServerProxy("http://localhost:8000/RPC2") as proxy:
            while True:
                try:
                    input_value = int(input("Enter a non-negative integer (or -1 to exit): "))
                    if input_value == -1:
                        break
                    result = proxy.calculate_factorial(input_value)
                    print(f"Factorial of {input_value} is: {result}")
                except ValueError as e:
                    print(f"Error: {e}")
    except ConnectionRefusedError:
        print("Error: Could not connect to server. Make sure the server is running.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    get_factorial()
