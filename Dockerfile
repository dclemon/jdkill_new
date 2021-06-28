FROM python:3.7-slim  
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin



ENV HOME=/root \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    SCRIPTS_DIR="/Scripts"
ADD ./code /scripts

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && cd /scripts \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple \
    && python -m pip install --upgrade pip \
    && pip install -r requirements.txt
WORKDIR ${SCRIPTS_DIR}
CMD ["python", "/scripts/LEMON.py"]