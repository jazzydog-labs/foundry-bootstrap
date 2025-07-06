# Container Environment

The development container used for testing runs **Ubuntu 24.04.2 LTS (Noble Numbat)**.
Python 3.12.10 is preinstalled along with the `pip` package manager.

To recreate a similar environment locally with Docker:

```Dockerfile
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3 python3-pip
```

You can then install the required Python packages using `pip install -r requirements.txt`.
