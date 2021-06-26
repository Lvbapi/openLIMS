from flask import render_template

from src import app


@app.errorhandler(404)
def page_not_found(e):
    return render_error_template(e, 404)


@app.errorhandler(405)
def bad_request_error(e):
    return render_error_template(e, 405)


def render_error_template(e, status_code):
    return render_template(
        "/error/error_template.html",
        status_code=status_code, error=e
    ), status_code
