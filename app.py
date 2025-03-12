from flask import Flask, request, render_template, redirect, url_for
from tasks.worker import scrape_broker
import time

app = Flask(__name__)

# Home page with input form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a URL.")

        # Start the scraping task
        task = scrape_broker.apply_async(args=[url])

        # Redirect to results page with the task ID
        return redirect(url_for("results", task_id=task.id))

    return render_template("index.html")

# Check and display results
@app.route("/results/<task_id>")
def results(task_id):
    task = scrape_broker.AsyncResult(task_id)

    # Wait for the task to finish (Polling)
    while not task.ready():
        time.sleep(1)

    # Handle errors correctly
    if task.failed():
        return render_template("results.html", error="Scraping failed. Please check the URL.")

    # Ensure task.result is a dictionary
    if isinstance(task.result, dict):
        return render_template("results.html", data=task.result)
    else:
        return render_template("results.html", error="Unexpected error occurred.")


if __name__ == "__main__":
    app.run(debug=True)
