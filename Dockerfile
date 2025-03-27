FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

# -----------------------------------------------------------------
# Copy certificates to make use of free open ai usage within the lab
# REMOVE THIS WHEN DEPLOYING TO CODE ENGINE

# Copy the self-signed root CA certificate into the container
COPY certs/rootCA.crt /usr/local/share/ca-certificates/rootCA.crt

# Update the CA trust store to trust the self-signed certificate
RUN chmod 644 /usr/local/share/ca-certificates/rootCA.crt && \
#  update-ca-certificates
# Set the environment variable OPENAI_API_KEY to empty string
ENV OPENAI_API_KEY=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
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
# -----------------------------------------------------------------

CMD ["python", "-u", "server.py"]