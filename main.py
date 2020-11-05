from os import environ
from re import search
from os import mkdir
from typing import Dict
from sys import exit


ENV_VARIABLE_PREFIX: str = "TOR_HIDDEN_SERVICE_"

KEY_REGEX: str = "^" + ENV_VARIABLE_PREFIX + "([a-zA-Z0-9]+)$"
ADDRESS_REGEX: str = "^([0-9]{1,5}) [a-zA-Z0-9.]+:([0-9]{1,5})$"
PRIVATE_KEY_REGEX: str = "-{3,}BEGIN RSA PRIVATE KEY-{3,}\n([\s\S]*?)\n-{3,}END RSA PRIVATE KEY-{3,}"

check_port = lambda port: 0 < port < 2**16

TOR_CONF_DIRECTORY: str = "/etc/torrc.d/"
TOR_DATA_DIRECTORY: str = "/var/lib/tor/hidden_services/"


if __name__ == "__main__":
    try:
        mkdir(TOR_DATA_DIRECTORY)
    except OSError:
        pass

    services: Dict[str, str] = {result.group(1): str(value) for key, value in environ.items() if (result := search(KEY_REGEX, key))}

    for key, value in services.items():
        print("[" + key + "] generating configuration...")

       
        service_id: str = key
        print("[" + key + "] calculated service id:", service_id) 

        private_key_key: str = ENV_VARIABLE_PREFIX + key + "_PRIVATE_KEY"
       
        with open(TOR_CONF_DIRECTORY + service_id, "w") as config_file:
            config_file_content: str = "HiddenServiceDir " + TOR_DATA_DIRECTORY + service_id + "/\n"

            for port_forwarding in value.split(";"):
                port_forwarding = port_forwarding.strip()
                if not (result := search(ADDRESS_REGEX, port_forwarding)):
                    print("[" + key + "] address does not match:", port_forwarding)
                    continue
                    
                try:
                    for port in result.groups():
                        if not check_port(int(port)):
                            print("[" + key + "] port not valid:", port)
                            continue
                except ValueError:
                    print("[" + key + "] port not found.")
                    continue

                config_file_content += "HiddenServicePort " + port_forwarding + "\n"

            config_file.write(config_file_content)

            print("[" + key + "] hostname will appear in", TOR_DATA_DIRECTORY + service_id + "/hostname") 

            try:
                mkdir(TOR_DATA_DIRECTORY + service_id)
            except OSError:
                print("[" + key + "] data already exists.") 
                continue

