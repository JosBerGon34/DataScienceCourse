# PostgreSQL Setup on CachyOS (Arch Linux) for Data Science Practice

## 1. Install PostgreSQL
```bash
sudo pacman -Syu
or
sudo pacman -S postgresql
```


## 2. Prepare Custom Data Directory on Samba Partition
*Ensure the partition is mounted at /run/media/josu/Samba
```bash
sudo mkdir -p /run/media/josu/Samba/postgres/data
sudo chown -R postgres:postgres /run/media/josu/Samba/postgres
sudo chmod 700 /run/media/josu/Samba/postgres/data

```

*Allow postgres user to traverse the path
```bash
sudo chmod +x /run/media/josu
sudo chmod +x /run/media/josu/Samba
```


## 3. Initialize Database Cluster
```bash
sudo -iu postgres initdb -D /run/media/josu/Samba/postgres/data --locale=C.UTF-8 --encoding=UTF8 --auth-local=peer --auth-host=scram-sha-256
```

## 4. Configure Systemd Service
*Create override file to point to custom directory and allow access to /run/media
```bash
sudo nano /etc/systemd/system/postgresql.service.d/override.conf
sudo mkdir -p /etc/systemd/system/postgresql.service.d
```


*Paste the following content into the file:
```bash
# [Service]

# Environment=PGROOT=/run/media/josu/Samba/postgres

# PIDFile=/run/media/josu/Samba/postgres/data/postmaster.pid

# ProtectHome=false

# PrivateTmp=false

```
*Save and exit (Ctrl+O, Enter, Ctrl+X)

## 5. Start and Enable Service
```bash

sudo systemctl daemon-reload
sudo systemctl enable --now postgresql
```


## 6. Create Database and User via psql
```bash
sudo -u postgres psql
```

*Inside psql prompt, run:
```sql
CREATE DATABASE "DataScienceCourse";
CREATE USER "Practice" WITH LOGIN PASSWORD '12345' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT;
GRANT CONNECT ON DATABASE "DataScienceCourse" TO "Practice";
GRANT ALL PRIVILEGES ON DATABASE "DataScienceCourse" TO "Practice";
\c "DataScienceCourse"
GRANT ALL ON SCHEMA public TO "Practice";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "Practice";
\q

```


## 7. Verify Connection Locally
```bash

PGPASSWORD=12345 psql -h 127.0.0.1 -U Practice -d DataScienceCourse -c "SELECT current_user, current_database();"

# Expected Output:

# current_user | current_database

# --------------+--------------------

# Practice | DataScienceCourse
```

 