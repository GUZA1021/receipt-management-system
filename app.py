from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import users, receipts
from application.user_application import UserApplication
from application.receipt_application import ReceiptApplication
from enums import UserRole, ReceiptStatus

app = Flask(__name__)
app.secret_key = "secretkey"


receipt_application = ReceiptApplication(receipts, users)
user_application = UserApplication(users)

@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        manager_id = request.form.get("manager_id")

        if role == "SALESMAN":
            if not manager_id:
                flash("Salesman must have a manager ID.")
                return render_template("register.html")
            
            manager = user_application.get_user(int(manager_id))

            if manager is None or not manager.is_manager():
                flash("Manager ID does not exsist")
                return render_template("register.html")
        else:
            manager_id = None

        user_application.create_user(username = username,name = name,
            email = email,password = password, role = role, manager_id = manager_id
        )

        
        flash(f"User {username} created!")
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    print("DEBUG: LOGIN ROUTE HIT WITH METHOD:", request.method)
    if "user" in session:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_application.validate_user(username, password)

        if user:
            session["user"] = user.id
            session["role"] = user.role.value

            if user.is_admin():
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("dashboard"))
        else:
            flash("Incorrect username or password")
            return redirect(url_for("login"))
            
        
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    user = get_current_user()

    if user is None:
        return redirect(url_for("login"))

    if user.is_salesman():
        show_receipts = receipt_application.get_user_receipt(user.id)
    elif user.is_accountant():
        show_receipts = receipt_application.get_by_status(ReceiptStatus.PENDING)
    elif user.is_manager():
        show_receipts = receipt_application.get_by_status(ReceiptStatus.HANDLED)
    elif user.is_admin():
        show_receipts = receipt_application.get_all()
    else:
        show_receipts = []
        
    return render_template("dashboard.html", user=user, receipts = show_receipts)

@app.route("/admin")
def admin_dashboard():
    user = get_current_user()
    
    if user is None:
        return redirect(url_for("login"))

    if not user.is_admin():
        return redirect(url_for("dashboard"))

    all_users = user_application.get_all_users()
    all_receipts = receipt_application.repo

    return render_template("admin_dashboard.html", user=user, users=all_users, receipts=all_receipts)

@app.route("/new_receipt", methods=["GET", "POST"])
def new_receipt():
    user = get_current_user()

    if user is None:
        return redirect(url_for("login"))
    
    if not user.can_submit():
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        amount = float(request.form.get("amount"))
        image = request.form.get("image_path")

        receipt_application.create_receipt(user.id, amount, image)
        flash("Receipt created!")
        return redirect(url_for("dashboard"))

    return render_template("new_receipt.html", user=user)

@app.route("/receipt/<int:receipt_id>")
def view_receipt(receipt_id):
    receipt = receipt_application.get_receipt(receipt_id)
    user = get_current_user()
    if user is None:
        return redirect(url_for("login"))
    
    if receipt is None:
        flash("Receipt does not exist.")
        return redirect(url_for("dashboard"))
    
    if not user.can_view(receipt):
        flash("You cannot view this receipt.")
        return redirect(url_for("dashboard"))
    
    return render_template("receipt_detail.html", user=user, receipt=receipt)


@app.route("/receipt/<int:receipt_id>/handle", methods=["POST"])
def handle_receipt(receipt_id):
    user = get_current_user()
    receipt = receipt_application.get_receipt(receipt_id)

    if not user.is_accountant():
        flash("Only accountants can handle receipts.")
        return redirect(url_for("dashboard"))

    if not user.can_handle(receipt):
        flash("You cannot handle this receipt.")
        return redirect(url_for("dashboard"))

    receipt_application.handle(receipt_id, user.id)
    flash(f"Receipt {receipt_id} is now handled")
    return redirect(url_for("dashboard"))


@app.route("/receipt/<int:receipt_id>/approve", methods=["POST"])
def approve_receipt(receipt_id):
    user = get_current_user()
    receipt = receipt_application.get_receipt(receipt_id)

    if not user.is_manager():
        flash("Only managers can approve receipts")
        return redirect(url_for("dashboard"))

    if not user.can_approve(receipt):
        flash("You cannot approcve this receipt")
        return redirect(url_for("dashboard"))

    receipt_application.approve(receipt_id, user.id)
    flash(f"Receipt {receipt_id} approved")
    return redirect(url_for("dashboard"))


@app.route("/receipt/<int:receipt_id>/reject", methods=["POST"])
def reject_receipt(receipt_id):
    user = get_current_user()
    receipt = receipt_application.get_receipt(receipt_id)

    if not user.is_manager():
        flash("Only managers can reject receipts.")
        return redirect(url_for("dashboard"))

    if not user.can_reject(receipt):
        flash("You cannot reject this receipt.")
        return redirect(url_for("dashboard"))
    
    receipt_application.reject(receipt_id, user.id)
    flash(f"Receipt {receipt_id} rejected")
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    if "user" in session:
        session.clear()
        flash("You have been logged out")
        return redirect(url_for("login"))
    
    return redirect(url_for("login"))

def get_current_user():
    user_id = session.get("user")
    if user_id is None:
        return None
    
    user = user_application.get_user(user_id)
    
    if user is None:
        session.clear()
        return None
        
    return user_application.get_user(user_id)

def clear_broken_session():
    user_id = session.get("user")
    if user_id is not None:
        user_obj = user_application.get_user(user_id)
        if user_obj is None:
            session.clear()

if __name__ == "__main__":
    app.run(debug=True)