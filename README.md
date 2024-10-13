# Simple Bare Bones DNS Server

This project implements a simple DNS server using Python 3.12, SQLite, and FastAPI. It allows you to create and manage DNS records through an API.

## Features

- Basic DNS server functionality
- SQLite database for storing DNS records
- FastAPI + HTMX + Tailwind for creating and managing DNS records

## Requirements

- Python 3.12 or higher
- Make
- UV

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/hyla96/dns_server.git
   cd dns_server
   ```

2. Install the required dependencies:
   ```
   $ make setup
   
   $ make install
   ```

## Usage

1. Start the DNS server:
   ```
   python main.py
   ```

## Console Output Example

Here's an example of what you will see in the console when running the DNS server:

<img src="./docs/records_management.png" alt="Console Output Screenshot">

## Dig Example

Here's an example of using dig to query your DNS server:

<img src="./docs/dig_result.png" alt="Dig Screenshot">

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.