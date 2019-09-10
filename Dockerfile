FROM tiagopeixoto/graph-tool

RUN pacman -S --noconfirm python-igraph \
			  python-networkx \
			  python-pytest \
			  python-pytest-cov
