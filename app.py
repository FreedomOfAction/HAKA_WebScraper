from flask import Flask, request, jsonify
from tasks.worker import scrape_broker
import logging

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def start_scrape():
    """API endpoint to start a scraping task."""
    data = request.get_json()
    if "url" not in data:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    task = scrape_broker.apply_async(args=[data["url"]])
    return jsonify({"task_id": task.id, "status": "Scraping started"}), 202

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    """Checks the status of a scraping task."""
    task = scrape_broker.AsyncResult(task_id)
    return jsonify({"task_id": task_id, "status": task.status}), 200

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    """Retrieves the result of a completed scraping task."""
    task = scrape_broker.AsyncResult(task_id)
    if task.state == "SUCCESS":
        return jsonify({"task_id": task_id, "data": task.result}), 200
    return jsonify({"task_id": task_id, "status": task.state}), 202

if __name__ == '__main__':
    app.run(debug=True)
