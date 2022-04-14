FROM ubuntu:18.04

COPY tester.so /data/tester.so

RUN chmod u+x /data/tester.so
ENTRYPOINT ["./data/tester.so", "0.0.0.0", "4000"]
