FROM python

RUN apt-get update && apt-get install -y zsh git
RUN chsh -s /usr/bin/zsh root

COPY .devcontainer/library-scripts/desktop-lite-debian.sh /tmp/library-scripts/
RUN bash /tmp/library-scripts/desktop-lite-debian.sh root
ENV DBUS_SESSION_BUS_ADDRESS="autolaunch:" \
    VNC_RESOLUTION="1440x768x16" \
    VNC_DPI="96" \
    VNC_PORT="5901" \
    NOVNC_PORT="6080" \
    DISPLAY=":1" \
    LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8"

ARG WORKDIR=/code
WORKDIR ${WORKDIR}
COPY requirements.txt ${WORKDIR}
RUN pip3 install -r requirements.txt
RUN playwright install

RUN git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh && cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc

ENTRYPOINT ["/usr/local/share/desktop-init.sh"]
CMD ["sleep", "infinity"]
