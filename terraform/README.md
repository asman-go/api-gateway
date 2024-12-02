# Разворачиваем приложение в облаке

1. Запрашиваем токен `export YC_TOKEN="$(yc iam create-token --folder-id b1gr7b87128mt4levqg1)"`
2. `make plan`
3. `make apply`

# Проверить, что все ОК

```
ssh -i ycvm yc-user@<Your-IP|Your-Domain>
docker ps -a
```

Должны увидеть наши контейнеры (`-a` ключ нужен чтобы увидеть все контейнеры, даже те, которые остановились по каким-то причинам)

Посмотреть логи контейнеров:

```
docker logs <container-id|container-name>
```

# Возможные ошибки

## Не можем подключиться по SSH

```
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
```

Решение — почистить known hosts:

```
rm ~/.ssh/known_hosts
```

## Не можем подключиться к docker

```
permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/containers/json": dial unix /var/run/docker.sock: connect: permission denied
```

Решение:

```
sudo chmod 666 /var/run/docker.sock
```

## Есть сомнения, что cloud-init сработал не так

Логи:

```
sudo cat /var/log/cloud-init-output.log
sudo cat /var/log/cloud-init.log
```
