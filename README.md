# Docker-skype

## Installation

### 1. Install Docker

If you haven't installed Docker yet, install it by running:

```
# Linux
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
chmod +x app/start.sh
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
# Web:
http://localhost:5000


# Curl
curl --request POST \
  --url http://localhost:5000/send \
  --header 'Content-Type: application/json' \
  --data '{
        "username": "YOUR_USERNAME",
        "password": "YOUR_PASSWORD",
        "recipient": "YOUR_RECIPIENT",
        "message": "YOUR MESSAGE"
    }'

# Curl example
curl --request POST \
  --url http://localhost:5000/send \
  --header 'Content-Type: application/json' \
  --data '{
        "username": "phamphu232",
        "password": "Abc@133",
        "recipient": "19:c27a25ca284943dd943628fd94f13a04@thread.skype",
        "message": "<at id=\"*\">all</at> <at id=\"8:phamphu232\">phamphu232</at> Hi Test"
    }'
```



