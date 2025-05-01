#Design a distributed application using RPC for remote computation where client submits an integer
# value to the server and server calculates factorial and returns the result to the client program.
from xmlrpc.server import SimpleXMLRPCServer

class FactorialServer:
    def calculate_factorial(self, n):
        try:
            n = int(n)
            if n < 0:
                raise ValueError("Input must be a non-negative integer.")
            return 1 if n == 0 else n * self.calculate_factorial(n - 1)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid input: {str(e)}")

if __name__ == "__main__":
    server = SimpleXMLRPCServer(('localhost', 8000))
    server.register_instance(FactorialServer())
    print("FactorialServer is ready to accept requests.")
    server.serve_forever()
