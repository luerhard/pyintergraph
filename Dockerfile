FROM ubuntu:xenial

RUN apt-get update

RUN apt-get install -y build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev zlib1g-dev openssl libffi-dev python3-dev python3-setuptools wget

RUN mkdir /tmp/Python37 && cd /tmp/Python37 && \
    wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz && \
    tar xvf Python-3.7.0.tar.xz && \
    cd /tmp/Python37/Python-3.7.0 && \
    ./configure --enable-optimizations && \
    make altinstall


# Adding the graph_tool resources to the image
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 612DEFB798507F25
RUN echo "deb http://downloads.skewed.de/apt/xenial xenial universe" | tee /etc/apt/sources.list.d/graph_tool.list
RUN echo "deb-src http://downloads.skewed.de/apt/xenial xenial universe" | tee /etc/apt/sources.list.d/graph_tool_src.list

RUN apt-get update

# Installing graph_tool and pip
RUN apt-get install -y python3-graph-tool python3-pip

# Installing dependencies for python-igraph
RUN apt-get install -y libigraph0-dev libxml2-dev zlib1g-dev

#python3-numpy has a problem with multiarray-imports so the pip version is used

RUN echo "alias python=python3.7" | tee -a /root/.bashrc
RUN echo "alias pip=pip3.7" | tee -a /root/.bashrc

# Installing python packages 
RUN pip3.7 install -U networkx python-igraph matplotlib pytest scipy numpy

RUN ln -s /usr/lib/python3/dist-packages/graph_tool/ /usr/local/lib/python3.7/site-packages

RUN apt-get -y remove python3-numpy
RUN apt-get clean



