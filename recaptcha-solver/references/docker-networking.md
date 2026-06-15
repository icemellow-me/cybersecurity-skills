# Docker Networking for Solver APIs

## Environment

- VPS: AWS EC2 (23.22.196.74), private IP 172.31.47.117
- Container hostname: `6b8afd1165da`
- Container IP: `172.17.0.4` (may change on restart)
- Docker bridge gateway: `172.17.0.1`
- Container capabilities: `CHOWN`, `DAC_OVERRIDE`, `FOWNER`, `SETGID`, `SETUID`, `SETPCAP` (NO NET_ADMIN, NO SYS_ADMIN)

## Docker Run Command

```bash
docker run -d \
  --name hermes \
  --restart unless-stopped \
  --privileged \
  -v ~/.hermes:/opt/data \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -p 8642:8642 \
  -p 8866:8866 \
  -p 8877:8877 \
  nousresearch/hermes-agent gateway run
```

## Port Exposure Checklist (In Order)

1. **Application binds to `0.0.0.0` inside container** — verified with `ss -tlnp`
2. **Docker `-p` flag in `docker run` command** — creates docker-proxy on host
3. **iptables NAT rule** — must route to the CORRECT container IP
4. **AWS security group** — must allow inbound TCP on the port
5. **Application actually responds** — test from inside first, then outside

## The NAT Mismatch Bug

**Symptom:** `curl 127.0.0.1:8866` on the HOST returns `Connection reset by peer`, but `curl localhost:8866` inside the container works fine.

**Root cause:** iptables NAT rules route to the wrong container IP.

```
# NAT says:  8866 → 172.17.0.2:8866
# But app runs in:  172.17.0.4:8866
# docker-proxy connects to .0.2, nothing is listening there → ECONNRESET
```

**This happens when:**
- Multiple containers share the Docker bridge network
- Container was restarted and got a new IP (Docker assigns IPs sequentially)
- A stale or duplicate container holds the old IP

## Diagnosis Commands (Host Side)

```bash
# Check NAT rules
sudo iptables -t nat -L -n | grep -E '8866|8877'

# Check all container IPs
docker inspect --format '{{.Name}} {{.NetworkSettings.IPAddress}}' $(docker ps -q)

# Check docker-proxy processes
sudo ss -tulpn | grep docker-proxy

# Test from host
curl -v http://127.0.0.1:8866/health

# Test from host to container directly
curl http://172.17.0.4:8866/health
```

## Diagnosis Commands (Container Side)

```bash
# Container IP
ip addr show eth0 | grep inet

# Listening ports
ss -tlnp | grep -E '8866|8877'

# Local test
curl http://localhost:8866/health

# Test from container's own IP
curl http://172.17.0.4:8866/health
```

## Fixes (Priority Order)

### 1. Stop Competing Containers
```bash
docker stop hermes2 hermes-abc57f8b  # other containers taking IPs
docker restart hermes                 # our container gets re-IP'd
```

### 2. Recreate Container
```bash
docker stop hermes && docker rm hermes
docker run -d --name hermes ...  # fresh start, gets first available IP
```

### 3. Use Docker Network Aliases
Create a custom network with fixed IPs:
```bash
docker network create --subnet=172.20.0.0/16 solternet
docker run --network solternet --ip 172.20.0.2 ...
```

### 4. Cloudflare Tunnel (Bypass Docker Networking)
If Docker port mapping is broken and can't be fixed:
```bash
cloudflared tunnel --url http://localhost:8877
# → https://random-words.trycloudflare.com
```

⚠️ Quick tunnel URLs change on restart. Use named tunnels for persistence.

## Why iptables Inside Container Doesn't Work

Even as root, the container lacks `NET_ADMIN` capability:
```
$ iptables -t nat -A OUTPUT -p tcp --dport 8866 -j DNAT --to-destination 172.17.0.4:8866
iptables: Permission denied (you must be root)
```

This is by design — Docker drops `NET_ADMIN` unless explicitly granted with `--cap-add=NET_ADMIN`.

## AWS Security Group

On EC2, the security group must allow inbound TCP on ports 8866 and 8877 from `0.0.0.0/0`.

Check: EC2 → Instances → Security tab → Security group → Inbound rules.

Even if Docker networking is perfect, AWS will silently drop packets at the security group level with no error on the host.
