import requests
from termcolor import colored

class SimpleSQLFinder:
    def __init__(self, target_url, payloads_file="payload.txt"):
        self.target_url = target_url
        self.payloads_file = payloads_file
        self.load_payloads()
        self.sql_error_messages_mysql = [
            "error in your SQL syntax",
            "MySQL server version for the right syntax to use",
            "supplied argument is not a valid MySQL",
            "You have an error in your SQL syntax",
            "Microsoft OLE DB Provider for SQL Server",
            "Unclosed quotation mark before the character string",
            "Syntax error converting the nvarchar value",
            
        ]
        self.sql_error_messages_postgresql = [
            "error in your SQL syntax",
            "PostgreSQL server version for the right syntax to use",
            "supplied argument is not a valid PostgreSQL",
            "You have an error in your SQL syntax",
           
        ]
        self.sql_error_messages_mssql = [
            "Unclosed quotation mark after the character string",
            "Microsoft OLE DB Provider for SQL Server",
            "Incorrect syntax near",
            
        ]

    def load_payloads(self):
        try:
            with open(self.payloads_file, "r") as file:
                self.payloads = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"{self.payloads_file} bulunamadı. Lütfen dosyanızı kontrol edin.")
            self.payloads = []

    def check_sql_injection(self):
        try:
            for payload in self.payloads:
                full_url = self.target_url + payload
                response = requests.get(full_url)
                if any(message in response.text for message in self.sql_error_messages_mysql):
                    print(colored(f"MySQL SQL AÇIĞI BULUNDU KULLANILAN PAYLOAD: {payload}", 'green'))
                elif any(message in response.text for message in self.sql_error_messages_postgresql):
                    print(colored(f"PostgreSQL SQL AÇIĞI BULUNDU KULLANILAN PAYLOAD: {payload}", 'green'))
                elif any(message in response.text for message in self.sql_error_messages_mssql):
                    print(colored(f"MSSQL SQL AÇIĞI BULUNDU KULLANILAN PAYLOAD: {payload}", 'green'))
                else:
                    print(colored(f"SQL AÇIĞI BULUNAMADI: {payload}", 'red'))
        except requests.RequestException as e:
            print(f"Error checking SQL Injection: {str(e)}")

if __name__ == "__main__":
    print(colored("***************************************", 'blue'))
    print(colored("**        SQL SCANNER          **", 'blue'))
    print(colored("***************************************\n", 'blue'))

    target_url = input(colored("Hedef linki girin: ", 'yellow'))
    sql_finder = SimpleSQLFinder(target_url)
    sql_finder.check_sql_injection()
