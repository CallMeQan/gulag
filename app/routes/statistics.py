from os import getenv
from flask import Blueprint, render_template
from flask import render_template
from flask_login import current_user, login_required

import datetime

from ..models import User, Run_History
from ..extensions import login_manager

# Month mapping
month_mapping = {
    1: "Jan", 2: "Feb",
    3: "Mar", 4: "Apr",
    5: "May", 6: "Jun",
    7: "Jul", 8: "Aug",
    9: "Sep", 10: "Oct",
    11: "Nov", 12: "Dec"
}

# Create instance
statistics_bp = Blueprint('statistics', __name__)

def get_months(current_month: int, current_year: int) -> list["tuple"]:
    """
    Current month in int. January is 1, February is 2,..., December is 12.
    - Return a list of tuple (str month, year) like.
    """
    six_months_from_now = []
    for i in range(5, -1, -1):
        month = current_month - i
        year = current_year
        if month <= 0:
            month = 12 + month
            year -= 1
        six_months_from_now.append((month, year))
    return six_months_from_now

# User loader to get user object from the session when a request is made
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Main
@statistics_bp.route("/graph", methods = ["GET", "POST"])
@login_required
def graph():
    user_id = current_user.user_id

    today = datetime.datetime.now()
    current_month = today.month
    current_year = today.year
    
    # Get list of data to put into graph
    six_months_from_now = get_months(current_month = current_month, current_year = current_year)
    six_month_distances = []
    six_month_nums = []
    six_month_calories = []
    for i in range(6):
        month_overall = Run_History.get_overall_month(user_id = user_id, month = six_months_from_now[i][0], year = six_months_from_now[i][1])
        six_month_distances.append(month_overall["total_distance"])
        six_month_nums.append(month_overall["total_run_num"])
        six_month_calories.append(month_overall["total_calories"])

    # Get overall data to put into achievement
    month_overall = Run_History.get_overall_month(user_id = user_id, month = current_month, year = current_year)
    month_distance = round(month_overall["total_distance"], 1)
    month_longest_run = round(month_overall["longest_run"], 1)
    month_pace = round(month_overall["fastest_pace"], 1)

    overall = Run_History.get_overall(user_id = user_id)
    
    total_distance = round(overall["total_distance"], 1)
    longest_run = round(overall["longest_run"], 1)
    fastest_pace = round(overall["fastest_pace"], 1)
    total_run_num = overall["total_run_num"]
    success_rate = overall["success_rate"]

    print(f"\n\n\n\n{six_month_distances}\n\n\n")
    return render_template('home/statistics.html', segment='index',
                           total_distance = total_distance, month_distance = month_distance,
                           longest_run = longest_run, month_longest_run = month_longest_run,
                           fastest_pace = fastest_pace, month_pace = month_pace,
                           total_run_num = total_run_num, success_rate = success_rate,
                           six_months_from_now = six_months_from_now, six_month_distances = six_month_distances,
                           six_month_nums = six_month_nums, six_month_calories = six_month_calories)