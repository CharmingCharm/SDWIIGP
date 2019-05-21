# Dockerfile for building the OJ-Judger
FROM ubuntu:bionic
LABEL maintainer="mchobbylong@gmail.com"
ENV LANG=C.UTF-8 \
	PYTHONUNBUFFERED=0

# Build up python3 environment
RUN apt update -y && apt install ca-certificates -y
ADD tuna-sources.list /etc/apt/sources.list
RUN apt update -y && apt install -y python3 python3-pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install python requirements.txt for oj
ADD requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Specific workdir
WORKDIR /oj

# Configure image itself
CMD ["python3", "manage.py", "judger"]
