# Локальное развертывание на 1 ноде

## Сборка образов

```bash
docker build -t swarm-demo-api-gateway:latest ./api-gateway

docker build -t swarm-demo-load-service:latest ./load-service

docker build -t swarm-demo-ml-service:latest ./ml-service

docker build -t swarm-demo-data-service:latest ./data-service

docker build -t swarm-demo-frontend:latest ./frontend
```

## Добавление конфигов и секретов

```bash
echo "appdb" | docker config create pg_db_name -

echo "postgres" | docker config create pg_db_user -

echo "secret-password" | docker secret create pg_password -
```

## Секреты и конфиги для редиса

```PowerShell
docker config create redis_conf redis.conf
```

У меня на win-10 креды для редиса передавались некоректно из-за \r в конце секрета, нашел такой выход

### Сначала создадим файлы секретов

```PowerShell
$app = "app"
$pass = "secret-password"
[System.IO.File]::WriteAllText("redis_app_username.txt", $app, [System.Text.UTF8Encoding]::new($false))
[System.IO.File]::WriteAllText("redis_app_password.txt", $pass, [System.Text.UTF8Encoding]::new($false))
```

### Потом создадим из них секреты

```PowerShell
docker secret create redis_app_username redis_app_username.txt
docker secret create redis_app_password redis_app_password.txt
```

## Деплой в Swarm

```bash
docker swarm init

docker stack deploy -c stack.yml demo
```

Проверка:

```bash
docker stack services demo
docker stack ps demo
docker service logs demo_api-gateway -f
```

Приложение будет доступно по адресу:

```text
http://<IP-manager-node>:8090
```

## Удаление

```bash
docker stack rm demo
```

# Диаграмма Монолита

```mermaid
flowchart LR
    U[Пользователь]

    subgraph SW[Docker Swarm cluster]
        direction LR

        subgraph ING[Ingress]
            T[Traefik]
        end

        subgraph APP[Application layer]
            direction LR
            F[Frontend]
            B[Backend]

        end

        subgraph ST[Data layer]
            direction TB
            DB[(PostgreSQL)]

        end
    end

    U -- HTTP --> T
    T -- HTTP --> F
    T -- HTTP --> B
    F -- HTTP --> B
    B -- HTTP --> DB

    subgraph LEG[Легенда]
        direction LR
        LG1[Сервис]
        LG2[Ingress]
        LG3[(Data storage)]
    end

    classDef container fill:#c8f7c5,stroke:#2e7d32,stroke-width:2px,color:#000;
    classDef proxy fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px,color:#000;
    classDef storage fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000;
    classDef usernode fill:#f5f5f5,stroke:#616161,stroke-width:2px,color:#000;

    class F,B,D,M,L,LG1 container;
    class T,LG2 proxy;
    class DB,R,LG3 storage;
    class U,LG4 usernode;
```

# Диаграмма Микросервисов

```mermaid
flowchart LR
    U[Пользователь]

    subgraph SW[Docker Swarm cluster]
        direction LR

        subgraph ING[Ingress]
            T[Traefik]
        end

        subgraph APP[Application layer]
            direction LR
            F[Frontend]
            B[API Gateway]
            D[Data Service]
            M[ML Service]
            L[Load Service]
        end

        subgraph ST[Data layer]
            direction TB
            DB[(PostgreSQL)]

        end
    end

    U -- HTTP --> T
    T -- HTTP --> F
    T -- HTTP --> B

    F -- HTTP --> B

    B -- HTTP --> D
    B -- HTTP --> M
    B -- HTTP --> L
    D -- HTTP --> DB

    subgraph LEG[Легенда]
        direction LR
        LG1[Сервис]
        LG2[Ingress]
        LG3[(Data storage)]
    end

    classDef container fill:#c8f7c5,stroke:#2e7d32,stroke-width:2px,color:#000;
    classDef proxy fill:#ffe0b2,stroke:#ef6c00,stroke-width:2px,color:#000;
    classDef storage fill:#bbdefb,stroke:#1565c0,stroke-width:2px,color:#000;
    classDef usernode fill:#f5f5f5,stroke:#616161,stroke-width:2px,color:#000;

    class F,B,D,M,L,LG1 container;
    class T,LG2 proxy;
    class DB,R,LG3 storage;
    class U,LG4 usernode;

```
