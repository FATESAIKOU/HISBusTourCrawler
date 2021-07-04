FROM adieuadieu/headless-chromium-for-aws-lambda:89.0.4389.128 AS headless-chrome-image

FROM amazon/aws-lambda-python:3.7
MAINTAINER FATESAIKOU
LABEL authors="FATESAIKOU <qzsecftbhhhh@gmail.com>"

# Install git wget unzip vim
RUN yum update -y && \
  yum install -y git wget unzip vim procps psmisc && \
  rm -Rf /var/cache/yum

# Install chromium
COPY --from=headless-chrome-image /bin/headless-chromium /var/task/bin/chromium

# Install chromedriver
RUN wget 'https://chromedriver.storage.googleapis.com/89.0.4389.23/chromedriver_linux64.zip' -O temp.zip && \
	unzip temp.zip && \
	mv chromedriver /var/task/bin/chromedriver

# Install python dependency
ADD requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt
RUN pip3 install -r requirements.txt

# Add /var/task/bin to $PATH
ENV PATH="${PATH}:/var/task/bin"

CMD [ "lambda_main.handler" ]
