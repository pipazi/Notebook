[返回目录](../README.md)
# Airflow
## Overview
* celery structure:
  ![avatar](../img/celeryStructure.png)

* strong airflow
  ![avatar](../img/strongAirflow.png)
  From: https://www.cnblogs.com/xiongnanbin/p/11836049.html
* celery worker
  ![avatar](../img/celery.png)
  From: https://airflow.apache.org/docs/stable/executor/celery.html
  
## Problems:
1. ModuleNotFoundError: No module named 'MySQLdb':
```bash
apt-get install libmysqlclient-dev & pip install mysqlclient==1.3.4 & pip install Flask-MySQLdb==0.2.0
```

2. password auth need install:
```bash
pip install Flask-Bcrypt
```

3. secret connnection need install:
```bash
pip install cryptography
```

4. Airflow change UI time (From: https://blog.csdn.net/crazy__hope/article/details/83688986): 

4.1 在airflow家目录下修改airflow.cfg，设置
```bash
default_timezone = Asia/Shanghai
```
4.2 修改airflow/utils/timezone.py

4.2.1 在 utc = pendulum.timezone(‘UTC’)代码下添加,
```python
from airflow import configuration as conf
try:
	tz = conf.get("core", "default_timezone")
	if tz == "system":
		utc = pendulum.local_timezone()
	else:
		utc = pendulum.timezone(tz)
except Exception:
	pass
```
4.2.2 修改utcnow()函数
```python
# d = dt.datetime.utcnow()
d = dt.datetime.now()
```

4.3 修改airflow/utils/sqlalchemy.py, 在utc = pendulum.timezone(‘UTC’)代码下添加:
```python
from airflow import configuration as conf
try:
	tz = conf.get("core", "default_timezone")
	if tz == "system":
		utc = pendulum.local_timezone()
	else:
		utc = pendulum.timezone(tz)
except Exception:
	pass
```

4.4 修改airflow/www/templates/admin/master.html
```html
<!--var UTCseconds = (x.getTime() + x.getTimezoneOffset()*60*1000); -->
var UTCseconds = x.getTime();

<!--"timeFormat":"H:i:s %UTC%",-->
"timeFormat":"H:i:s",
```

4.5 注释airflow/utils/sqlalchemy.py中的:
```html
cursor.execute(“SET time_zone = ‘+00:00’”)
```


5. ImportError: libpq.so.5: cannot open shared object file: No such file or directory:
```bash
apt install libpq-dev
```

6. Move virtue-python-env to other env and Source active not working:
*change dir in active*

7. Airflow change email method:
add blew code to utils/email.py
```python
from exchangelib import DELEGATE, Account, Credentials, Message, Mailbox, FileAttachment, NTLM, HTMLBody
from exchangelib.configuration import Configuration


def send_email_exchange(to, subject, html_content, files=None,
                        dryrun=False, cc=None, bcc=None,
                        mime_subtype='mixed', mime_charset='utf-8',
                        **kwargs):
    # account, subject, body, recipients, attachments=None
    """
    Send an email.

    Parameters
    ----------
    account : Account object
    subject : str
    body : str
    recipients : list of str
        Each str is and email adress
    attachments : list of tuples or None
        (filename, binary contents)

    Examples
    --------
    # >>> send_email('test@example.com', 'foo', '<b>Foo</b> bar', ['/dev/null'], dryrun=True)
    >>> send_email(account, 'Subject line', 'Hello!', ['info@example.com'])
    """


    to = get_email_address_list(to)

    to_recipients = []
    for recipient in to:
        to_recipients.append(Mailbox(email_address=recipient))

    # Get sender account info
    exchange_mail_from = conf.get('exchange', 'exchange_mail_from')
    exchange_server = conf.get('exchange', 'exchange_server')
    exchange_username = conf.get('exchange', 'exchange_username')
    exchange_password = conf.get('exchange', 'exchange_password')

    credentials = Credentials(
        username=exchange_username,  # Or myusername@example.com for O365
        password=exchange_password
    )
    config = Configuration(server=exchange_server, credentials=credentials, auth_type=NTLM)
    account = Account(
        primary_smtp_address=exchange_mail_from,
        config=config,
        autodiscover=False,
        access_type=DELEGATE
    )

    # Create message
    m = Message(account=account,
                folder=account.sent,
                subject=subject,
                body=HTMLBody(html_content),
                to_recipients=to_recipients)

    # attach files
    for fname in files or []:
        basename = os.path.basename(fname)
        with open(fname, "rb") as f:
            content = f.read()
        file = FileAttachment(name=basename, content=content)
        m.attach(file)

    if not dryrun:
        m.send_and_save()
```

8. log request 503:
  ```bash
  unset http_proxy
  unset https_proxy
  ```

9. check airflow health:
  *webserver_url/health*
  
10. mutate tasks:
  *$ARIRFLOW_HOME/airflow_local_settings.py*
  
## Config
airflow.cfg:
```editorconfig
[core]
# Auto update/push with gitlab
dags_folder = /dir_to_dags
# change log file name because execution time could be wrong
log_filename_template = {{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log
# change timezone
default_timezone = Asia/Shanghai
# change executor
executor = CeleryExecutor
# change sqlalchemy connect url
sql_alchemy_conn = postgresql+psycopg2://usrname:password@host:port/databse
# disable example
load_examples = False
[webserver]
# web server url
base_url = http://ip:port
# ui time, basic flask server have to be changed source code
default_ui_timezone = Asia/Shanghai
# web server port number
web_server_port = port
# used for password_auth
authenticate = True
auth_backend = airflow.contrib.auth.backends.password_auth
rbac = False
# used for rbac
# security = Flask AppBuilder
# secure_mode = True
# rbac = True
[celery]
# set log server port
worker_log_server_port = $worker_log_server_port
# celery need a broker server, can be redis or rabbitmq
broker_url = redis://host:port/database
# meta database for celery
result_backend = db+postgresql://username:password@host:port/database
# celery monitor server's port
flower_port = $flower_port
[celery_broker_transport_options]
# set celery worker timout
visibility_timeout = 18000
[scheduler]
# set to false to prevent scheduler execute past task
catchup_by_default = False
# change load dag dir frequency
dag_dir_list_interval = 10
[scheduler_failover]
# get through command 'scheduler_failover_controller get_current_host'
scheduler_nodes_in_cluster = $node_name
# change restart scheduler env
airflow_scheduler_start_command = export AIRFLOW_HOME=/dir_to_airflow/airflow;nohup airflow scheduler >> ~/dir_to_log/scheduler.logs &
[dag_creation_manager]
# queue name
dag_creation_manager_queue_pool = default_pool:default_pool|default_pool
[email]
# change from stmp to exchange
email_backend = airflow.utils.email.send_email_exchange
[exchange]
exchange_mail_from = XXX
exchange_server = XXX
exchange_username = XXX
exchange_password = XXX
```
