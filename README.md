![Newman](https://github.com/zoumpatianos/newman/raw/master/docs/img/newman.png "Newman logo")  
# Newman mailer app
Newman provides an HTTP service that processes email jobs.
Currently, it supports 3 email service backends:
- Mailgun
- Sendgrid
- Sparkpost

Emails are queued in a beanstalkd queue and processed by multiple workers in parallel.

## Trivia
- Its name is chosen in the nameshake of the [postman character in the Seinfeld TV series](https://en.wikipedia.org/wiki/Newman_(Seinfeld)).
- It is written by [Kostas Zoumpatianos](mailto:zoumbatianos@gmail.com).

## Architecture
Newman's architecture can be seen below.

```               
                 =================             Workers              Backends
    Client ====> | HTTP frontend | 
                 =================                                ==============
                        ||                    [Worker 1]  --->    |            |
                        ||                  /                     |  Mailgun   |
                        ||                 /  [Worker 2]  --->    |  Sendgrid  |
                        ||                / /                     |  Sparkpost |
                        \/               / /     ...              |     ...    |
             ===========================/ /                       |            |
             | Beanstalkd queue server |----- [Worker n]  --->    ==============
             ===========================
```

## Prerequisites
To run newman you need to install [beanstalkd](https://beanstalkd.github.io/) and various python libraries.
The process is described in detail below.

### Beanstalkd installation guide
Beanstalkd exists in most major linux distributions, as well as in homebrew.
It has been developed by [Causes.com](https://www.causes.com), with performance being its main goal (more information here: https://beanstalkd.github.io/)

#### Ubuntu Linux
```bash 
sudo apt-get install beanstalkd
```

#### Fedora Linux
```bash 
sudo dnf install beanstalkd
```

#### Mac OS X / Homebrew
```bash
brew install beanstalkd
```

In order to start the beanstalkd service on linux, issue the following command.
```sudo service beanstalkd start```

#### Fault tolerance
Please keep in mind that if you start beanstalkd with the -b option, jobs are persisted.
As a result, increased **fault tolerance** can be achieved.

### Python libraries
Newman uses: sanic, greenstalk, sparkpost, and requests.
Those can be installed as follows:

```sudo pip3 install sanic greenstalk sparkpost requests```

## Using newman

### Configuration
Newman's configuration exists in the **newman/config.py** file.
In this file, all API keys, ports, hostnames, as well as other properties can be set.

```python
Configuration = {
    "DEFAULT": {
        "MessageBroker": {"host": "0.0.0.0", "port": 11300},
        "HttpFrontend": {"host": "0.0.0.0", "port": 8080, "debug": False},
        "Backends": {
            "MailGun": {
                "ACTIVE": True,
                "MAILGUN_API_KEY": "",
                "MAILGUN_SANDBOX_URL": "" 
            }, 
            "SendGrid": {
                "ACTIVE": True,
                "SENDGRID_API_KEY": ""
            },
            "SparkPost": {
                "ACTIVE": True,
                "SPARKPOST_API_KEY": ""
            }
        },
        "Workers": 10
    }
}
```

- MessageBroker refers to the beanstalkd instance.
- HttpFrontend is the public HTTP API.
- Backends are the set of email service backends. 
- By setting the active property to true or false you can activate and deactivate them.
- Workers defines the number of workers that we want to spawn in parallel.


## Running newman
One can use the two scripts that exist in the bin/ directory for starting the HTTP frontend and the workers.

### Starting the workers
To start the workers, type:
```
PYTHONPATH=. ./bin/start_workers
```

This will spawn one thread for each worker.

### Starting the frontend
To start the frontend, type:
```
PYTHONPATH=. ./bin/start_frontend
```


The system should now be live.

### Monitoring 
By default newman uses a file based monitoring module. This creates one file per thread.
The format of each file is a semicolon separated text file.
To monitor the files' contents as the system is running, one can issue the following command:

```bash
watch "cat monitoring.* | sed 's/;/\t/g' | column -t | sort"
```

This produces the following output:
![Result screenshot](https://github.com/zoumpatianos/newman/raw/master/docs/img/screenshot1.png "Result screenshot")


## Using newman
Email requests can be sent using HTTP get calls to newman.

They should follow the format bellow:

```
curl http://0.0.0.0:8080?from=zoumbatianos@gmail.com&\
                         to=kostas@seas.harvard.edu&\
                         subject=Testmail&\
                         body=Testbody
```
The formant contains 4 get arguments:
- from: the email of the sender
- to: a target email (this can be repeated more than once for multiple recipients)
- subject: the subject
- body: the email body

### Multiple destinations
By adding multiple ``to`` arguments, one can send an email to multiple recipients
```
curl http://0.0.0.0:8080?from=zoumbatianos@gmail.com&\
                         to=kostas@seas.harvard.edu&\
                         to=kostas@scientifreak.com&\
                         subject=Testmail&\
                         body=Testbody
```

### Expected output
Once a request is sent, a json response will be provided.
In case of success it will have the following form:
```json
{"status": "sending",
 "errors": []}
 ```

In case of failure it will look like that:
```json
{"status": "error",
 "errors": ["error 1", "error 2 ..."]}
 ```

 
If the status is set to "sending", this means that the email has ben queued and will be soon processed by a worker.

## Testing
Tests are provided in the **tests/** folder. To run them issue the following command:

```bash
PYTHONPATH=. python3 tests/test_newman.py
```

## Performance
In terms of response time, newman has been tested with apachebench.
Running apache bench for 10k requests and 1k concurrent connections, yielded a performance of >1000 requests per second.
In terms of end-to-end execution time, the amount of workers determines how fast the submitted jobs are going to be processed. 
Newman's architecture can scale horizontally, as more workers can be added running in one or more machines, sending emails in parallel.

The results of the aforementioned ab benchmark can be seen bellow.
```
Concurrency Level:      1000
Time taken for tests:   7.761 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      1220000 bytes
HTML transferred:       320000 bytes
Requests per second:    1288.54 [#/sec] (mean)
Time per request:       776.075 [ms] (mean)
Time per request:       0.776 [ms] (mean, across all concurrent requests)
Transfer rate:          153.52 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   99 298.3      3    1064
Processing:    11  276 897.4     83    6722
Waiting:        1  268 898.3     76    6720
Total:         15  376 1121.7     86    7738

Percentage of the requests served within a certain time (ms)
  50%     86
  66%     90
  75%     93
  80%     97
  90%    148
  95%   2768
  98%   4447
  99%   7734
 100%   7738 (longest request)
```

