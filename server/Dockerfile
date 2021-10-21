From tensorflow/tensorflow

WORKDIR /app/src
COPY . /app

#ENV TF_XLA_FLAGS --tf_xla_cpu_global_jit
#RUN mkdir -p /root/.keras/models && mv /app/src/data/models/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5 /root/.keras/models/
#RUN wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip

RUN apt-get update && apt-get install python3-pip python3 -y
RUN pip3 install -r /app/requirements.txt
EXPOSE 5001

CMD python3 main.py