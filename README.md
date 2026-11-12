### собрать проект по Dockerfile (-t это тэг)
sudo docker build -t day2-agent .

### запустить контейнер (-rm что бы удалять контейнер после завершения (не засирать память))
sudo docker run --rm day2-agent

### запускаем поисковика уязвимостей "Триви" (-v соединяем 2 докер сокета двух образов что бы они могли видеть друг друга)
sudo docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image day2-agent

### почистить мусор 
sudo docker system prune -f