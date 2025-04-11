# Asteroids
*Asteroids game - Python and SimpleGui*

This game uses the `simplegui` package

**Install Simplegui (Windows)**

I develop this game under Window operating system. I installed
<a href="https://pypi.python.org/pypi/SimpleGUITk/1.1.3" target="_blank">Simpleguitk</a> following this steps:

1. Install python 3.13
2. Install <a href="http://www.pygame.org/download.shtml" target="_blank">pygame</a>
`py -m pip install -U pygame --user`
3. Install <a href="https://pypi.python.org/pypi/SimpleGUITk" target="_blank">Simpleguitk</a> `py -m pip install SimpleGUITk`

**Install Simplegui (Linux)**

1. Install python 3.13
2. Install <a href="http://www.pygame.org/download.shtml" target="_blank">pygame</a>
3. Install <a href="https://pypi.python.org/pypi/SimpleGUICS2Pygame" target="_blank">simplegui</a>

**Use**

1. Upload the resources folder to a local or remote server. The source includes a Dockerfile that inits this server with the resources; just run:

`docker build -t asteroids-resources .`

`docker run -d --rm -p 8083:8083 asteroids-resources`

2. Run and Play!

`py asteroids.py`

