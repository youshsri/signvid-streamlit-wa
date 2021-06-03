FROM python:3.8.3
WORKDIR /app
COPY requirements.txt ./requirements.txt
COPY s2s_wa_v2.py ./s2s_wa_v2.py
RUN pip3 install -r requirements.txt
EXPOSE 8080
COPY . /app
CMD streamlit run --server.port 8080 --server.enableCORS false signvid.py 