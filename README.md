# docky-onion

You have a normal service and want to bring it into the tor network now? Then you've come to the right place! Come in and have a look around!

## docker-compose


```yaml
version: "3.7"

services:
  docky-onion:
    image: useto/docky-onion
    restart: always
    environment:
      # this forwards 80 and 8080 to web:80
      TOR_HIDDEN_SERVICE_WEB: "80 web:80;8080 web:80"
    volumes:
      - "docky-onion:/var/lib/tor/hidden_services"
    depends_on:
      - web

  web:
    image: nginx
    restart: always

volumes:
  docky-onion:
```

After you have started the container you can read the `.onion`-addresses as follows:

`$ docker-compose exec tor lookup `
`WEB => j3c7wmyv6b3q3uvowetwwygb7h57k2bjhtnwp2zfamda2ij2vanyhmid.onion`

