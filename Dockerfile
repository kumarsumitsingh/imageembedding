# Use AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.9

# Set working directory
WORKDIR /var/task

# Install necessary system dependencies
RUN yum update -y && \
    yum install -y \
        gcc gcc-c++ make wget tar gzip libstdc++-devel \
        automake autoconf libtool pcre2-devel \
        bison flex byacc && \
    yum clean all && \
    rm -rf /var/cache/yum

# Install SWIG 4.1.0 manually
RUN wget https://github.com/swig/swig/archive/refs/tags/v4.1.0.tar.gz && \
    tar -xvzf v4.1.0.tar.gz && \
    cd swig-4.1.0 && \
    ./autogen.sh && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf swig-4.1.0 v4.1.0.tar.gz

# Verify SWIG version
RUN swig -version

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy function code
COPY embeddings.py .

# Set the CMD to your handler
CMD ["embeddings.handler"]
