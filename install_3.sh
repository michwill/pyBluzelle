#!/bin/bash

PROTO_BASE="https://raw.githubusercontent.com/bluzelle/swarmDB/master/proto"

# Download proto files
wget "$PROTO_BASE/audit.proto" -O proto/audit.proto
wget "$PROTO_BASE/bluzelle.proto" -O proto/bluzelle.proto
wget "$PROTO_BASE/database.proto" -O proto/database.proto
wget "$PROTO_BASE/pbft.proto" -O proto/pbft.proto

# Compile proto
protoc --python_out=./pyBluzelle/proto --proto_path=proto proto/pbft.proto proto/bluzelle.proto proto/database.proto proto/audit.proto

# Solve Python3 incompatibility
sed -i 's/import database_pb2/import pyBluzelle.proto.database_pb2/g' pyBluzelle/proto/pbft_pb2.py
sed -i 's/import database_pb2/import pyBluzelle.proto.database_pb2/g' pyBluzelle/proto/bluzelle_pb2.py
sed -i 's/import audit_pb2/import pyBluzelle.proto.audit_pb2/g' pyBluzelle/proto/bluzelle_pb2.py
sed -i 's/import pbft_pb2/import pyBluzelle.proto.pbft_pb2/g' pyBluzelle/proto/bluzelle_pb2.py

# Create virtualenv and install there
mkdir .venv
virtualenv .venv -p python3
source .venv/bin/activate
pip3 install -r requirements.txt
pip3 install -e .  # Editable installation for development only
