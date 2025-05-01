# PROBLEM STATEMENT: -
# Design a distributed application using RMI for remote computation where client submits two strings to
# the server and server returns the concatenation of the given strings.


## Before starting server make sure to run following command in new terminal 
## "python -m Pyro4.naming"
## and then run the server code and client code in different terminals

import Pyro4
import sys

@Pyro4.expose
class StringConcatenationServer:
    def concatenate_strings(self, str1, str2):
        result = str1 + str2
        return result

def main():
    try:
        daemon = Pyro4.Daemon()  # Create a Pyro daemon
        try:
            ns = Pyro4.locateNS()  # Locate the Pyro nameserver
        except Pyro4.errors.NamingError:
            print("Error: Could not locate the Pyro nameserver.")
            print("Please make sure the nameserver is running by executing:")
            print("python -m Pyro4.naming")
            sys.exit(1)
            
        # Create an instance of the server class
        server = StringConcatenationServer()
        # Register the server object with the Pyro nameserver
        uri = daemon.register(server)
        ns.register("string.concatenation", uri)
        print("Server URI:", uri)
        with open("server_uri.txt", "w") as f:
            f.write(str(uri))
        print("Server is ready. Press Ctrl+C to exit.")
        daemon.requestLoop()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

