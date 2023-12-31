# Docker-skype

## Installation

### 1. Install Docker

If you haven't installed Docker yet, install it by running:

```
sudo curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $(whoami)
exit
```

### 2. Clone source code

```
git clone https://github.com/phamphu232/docker-skype.git docker-skype
```

### 3. Create docker container

```
cd docker-skype
docker compose up -d
```

### 4. Start/Stop/Restart/Remove/Statistics docker skype

```
# Start
docker compose start

# Stop
docker compose stop

# Restart
docker compose restart

# Remove
docker compose down

# Statistics
docker stats
```

### 5. Result

```
http://localhost:5000
```



