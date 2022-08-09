docker build -t discord_notifier .
docker-compose up -d
set YOUR_IP:8088 as receiver in your prometheus alertmanager
