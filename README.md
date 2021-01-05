# docky-onion

You have a normal service and want to bring it into the tor network now? Then you've come to the right place! Come in and have a look around!

## docker-compose


```yaml
version: "3.3"

services:
  docky-onion:
    build: .
    restart: always
    environment:
      # this forwards 80 and 8080 to web:80
      TOR_HIDDEN_SERVICE_WEB: "80 web:80;8080 web:80"

      # this forwards only 6667 irc:6667
      TOR_HIDDEN_SERVICE_IRC: "6667 irc:6667"
    volumes:
      - "docky-onion:/var/lib/tor/hidden_services"

  web:
    image: nginx
    restart: always
    depends_on:
      - docky-onion

  irc:
    image: inspircd/inspircd-docker
    restart: always
    depends_on:
      - docky-onion

volumes:
  docky-onion:
```

After you have started the container you can read the `.onion`-addresses as follows:

`$ docker-compose exec docky-onion lookup`  
```
IRC => a3s3dfyaruqjq6exi76ivtnjv77qkjnfkaoaw5rlyj5a4id2zrkxaoyd.onion
WEB => j3c7wmyv6b3q3uvowetwwygb7h57k2bjhtnwp2zfamda2ij2vanyhmid.onion
```

