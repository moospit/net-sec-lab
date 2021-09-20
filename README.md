# ARP Cache Poisoning Lab

This repository contains a minimal lab setup for demoing ARP cache poisoning.

## Setup

- Install `docker` and `docker-compose`
- Clone this repo
- Run `./build.sh`

You get two images for

- victim
- attacker

that are used by the containers describes in the next section.

After the images are built, run the containers via the command:

```bash
$ docker-compose up -d
[+] Running 0/3
 ⠋ Container alice  Creating
 ⠋ Container evie   Creating
 ⠋ Container bob    Creating
 ...
```

## Configuration

There are three containers based on two images

| Name    | IP address  | MAC address       | Role     |
| ------- | ----------- | ----------------- | -------- |
| `alice` | 10.10.0.101 | 00:00:00:00:00:01 | Victim   |
| `bob`   | 10.10.0.102 | 00:00:00:00:00:02 | Victim   |
| `evie`  | 10.10.0.103 | 00:00:00:00:00:03 | Attacker |

## Manual ARP Cache Poisoning

Tell `alice` that the ip address of `bob` resides at `evies` mac address.

```bash
$ scapy
...
>>> a = ARP()
>>> a.show()
>>> a.pdst('10.10.0.101')
>>> a.psrc('10.10.0.102')
```

During the attack, control the system's ARP cache for changes via

```bash
$ watch -d -n1 "ip neigh show"
Every 1.0s: ip neigh show

10.10.0.102 dev eth0 lladdr 00:00:00:00:00:02 REACHABLE
...
```

## Automatic ARP Cache Poisoning

> Notes for `spoofing.py`:
>
> - Reports captured HTTP data twice (bug in async. sniffer?)
> - Sometimes packets are not captured (bug in async. sniffer?)

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

## Common docker commands

### Control containers

```bash
# Bring containers up
$ docker-compose up -d
# Show logs of all containers
$ docker-compose logs -f
# Bring all containers down
$ docker-compose down
...
```

### List running containers

```bash
$ docker ps
CONTAINER ID   IMAGE             COMMAND            CREATED              STATUS              PORTS     NAMES
9e7773fe5b5f   arplab-attacker   "bash"             About a minute ago   Up About a minute             evie
ec2daae008fa   arplab-victim     "python3 app.py"   About a minute ago   Up About a minute             alice
ccd77adca40f   arplab-victim     "python3 app.py"   About a minute ago   Up About a minute             bob
```

### Accessing a containers

Start a shell in one of the containers (by name of the container):

```bash
$ docker exec -it evie /bin/bash
root@evie:/#
```
