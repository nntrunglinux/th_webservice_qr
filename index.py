from flask import render_template, request
from app import app
from app.purchase_order import purchase_order

@app.route("/po")
def get_purchase_order():
    po_number = request.args.get("id")
    po = purchase_order(po_number)
    return render_template("purchase_order_form.html", po=po)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
