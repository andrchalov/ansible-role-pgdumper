## Ansible role for scheduling pd_dump events.

#### Features:
  * removing old backups
  * pushing notifications by telegram bot about backup events

#### Supported configuration variables:

* **pgdumper_dir** - pgdumper directory location
* **pgdumper_jobs** - list of backup jobs, items format:
  * name - custom name of backup job
  * pgdump_args - list of arguments for pg_dump
  * m (optional) - minute in crontab format, \* by default
  * h (optional) - hour in crontab format, \* by default
  * dom (optional) - day of month in crontab format, \* by default
  * mon (optional) - month in crontab format, \* by default
  * dow - day of week in crontab format, \* by default
* **pgdumper_store_days** - how much days dumps should be stored
* **pgdumper_pgpass** (optional) - list of .pgpass file lines
* **pgdumper_telegram** (optional) - telegram notifications settings
  * **bot_api_key**
  * **channel**
* **pgdumper_log_prefix** (optional) - prefix for log messages


#### Example configuration:

```yaml
pgdumper_dir: /data/pgdumper
pgdumper_jobs:
  - name: postgres database daily dump in 00:00
    pgdump_args:
      - "-U postgres -d postgres -h localhost -Z 5"
      - "-f dump_$(date +"\%Y\%m\%d_\%H\%M\%S").sql.gz"
    m: "0"
    h: "0"
pgdumper_store_days: 5
pgdumper_pgpass:
  - "localhost:5432:*:postgres:{{password}}" # use ansible vault for secure
pgdumper_telegram:
  bot_api_key: [BOT_API_KEY]
  channel: [CHANNEL_NAME]
```
