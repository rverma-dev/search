FROM tensorflow/tensorflow:2.4.3
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --use-feature=2020-resolver -r /app/requirements.txt
ENV TF_XLA_FLAGS --tf_xla_cpu_global_jit
COPY ./src/ /app
EXPOSE 5001
CMD python3 main.py