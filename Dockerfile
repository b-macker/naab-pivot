FROM ubuntu:22.04

LABEL org.opencontainers.image.source="https://github.com/b-macker/naab-pivot"
LABEL org.opencontainers.image.description="NAAb Pivot - Polyglot Code Evolution & Optimization"
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    # Go compiler
    golang-1.21 \
    # Rust compiler
    rustc \
    cargo \
    # C++ compiler
    g++ \
    clang \
    # Python
    python3 \
    python3-pip \
    # Ruby
    ruby \
    ruby-dev \
    # Node.js
    nodejs \
    npm \
    # PHP
    php \
    php-cli \
    # Julia (install separately)
    && rm -rf /var/lib/apt/lists/*

# Set up Go PATH
ENV PATH="/usr/lib/go-1.21/bin:${PATH}"

# Install Zig
RUN wget https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz && \
    tar -xf zig-linux-x86_64-0.11.0.tar.xz && \
    mv zig-linux-x86_64-0.11.0 /opt/zig && \
    rm zig-linux-x86_64-0.11.0.tar.xz
ENV PATH="/opt/zig:${PATH}"

# Copy naab-pivot repository
WORKDIR /opt
COPY . /opt/naab-pivot

# Initialize and build NAAb submodule
WORKDIR /opt/naab-pivot
RUN git submodule update --init --recursive || true
RUN bash build.sh

# Add naab-lang and naab-pivot to PATH
ENV PATH="/opt/naab-pivot/naab/build:${PATH}"
ENV PIVOT_HOME="/opt/naab-pivot"

# Set working directory for user code
WORKDIR /workspace

# Create volumes for workspace and vessels
VOLUME ["/workspace", "/opt/naab-pivot/vessels"]

# Default command shows help
CMD ["/opt/naab-pivot/naab/build/naab-lang", "/opt/naab-pivot/pivot.naab", "--help"]
