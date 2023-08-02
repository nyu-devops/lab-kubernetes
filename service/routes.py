# Copyright 2015, 2022 John J. Rofrano All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Redis Counter Demo in Docker
"""
from flask import jsonify, abort, url_for
from service import app
from service.common import status  # HTTP Status Codes
from service.models import Counter


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return {"status": 'OK'}, status.HTTP_200_OK


############################################################
# Home Page
############################################################
@app.route("/")
def index():
    """Home Page"""
    return app.send_static_file("index.html")


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """Lists all counters in the database"""
    app.logger.info("Request to list all counters...")
    counters = Counter.all()
    return jsonify(counters)


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Reads a counter from the database"""
    app.logger.info("Request to Read counter: %s...", name)

    counter = Counter.find(name)
    if not counter:
        abort(status.HTTP_404_NOT_FOUND, f"Counter [{name}] does not exist")

    app.logger.info("Returning: %d...", counter.value)
    return jsonify(counter.serialize())


############################################################
# Create counter
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Creates a counter in the database"""
    app.logger.info("Request to Create counter...")
    counter = Counter.find(name)
    if counter is not None:
        return jsonify(code=409, error=f"Counter [{name}] already exists"), 409

    counter = Counter(name)

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(counter.serialize()),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Updates a counter in the database"""
    app.logger.info("Request to Update counter...")
    counter = Counter.find(name)
    if counter is None:
        return (
            jsonify(code=404, error=f"Counter [{name}] does not exist"),
            404,
        )

    count = counter.increment()

    return jsonify(name=name, counter=count)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Removes te counter from teh database"""
    app.logger.info("Request to Delete counter...")
    counter = Counter.find(name)
    if counter:
        del counter.value

    return "", status.HTTP_204_NO_CONTENT
