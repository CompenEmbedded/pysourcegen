# Copyright 2024 Compen Embedded B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Toolchains for testing every pysourcegen generator. The repository is not
# copied in: mount it at /src (read-only is fine).
#
#   docker build -t pysourcegen-test docker/
#   docker run --rm -v "$PWD:/src:ro" pysourcegen-test

FROM mcr.microsoft.com/dotnet/sdk:10.0

ENV DEBIAN_FRONTEND=noninteractive \
    DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_NOLOGO=1 \
    GOTOOLCHAIN=local \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 python3-coverage \
        gcc g++ libc6-dev \
        rustc rustfmt \
        golang-go \
        nodejs npm \
        default-jdk-headless \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g typescript@5 @types/node \
    && npm cache clean --force

# A restored console project, so C# tests need no network access
RUN dotnet new console -o /opt/csapp \
    && dotnet build /opt/csapp

WORKDIR /src
CMD ["sh", "tests/integration/run.sh"]
