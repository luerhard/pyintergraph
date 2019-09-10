FROM tiagopeixoto/graph-tool

RUN pacman -S --noconfirm python-igraph python-pip

RUN pip install networkx pytest pytest-cov
