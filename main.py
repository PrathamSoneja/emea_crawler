import json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from fileinput import filename
from crawler__ee import process_cpw_ee
from crawler_currys import process_curry

# Flask constructor
app = Flask(__name__)


# Root endpoint
@app.get("/")
def upload():
    return render_template("index_1.html")


@app.route("/view", methods=["POST", "GET"])
def view():
    # Read the File using Flask request
    reg = request.form["region"]
    file_1 = request.files["first-file"]
    file_2 = request.files["second-file"]

    # save file in local directory
    # file_1.save(file_1.filename)
    # file_2.save(file_2.filename)

    # Parse the data as a Pandas DataFrame typecolumns
    df_1 = pd.read_excel(file_1)
    df_2 = pd.read_excel(file_2)
    print(reg)
    if reg == "CPW-uk" or reg == "ee-uk":
        col_1, col_2, missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1 = process_cpw_ee(df_1, df_2)
    elif reg == "currys-uk":
        col_1, col_2, missing_dv_1, missing_dv_2, disc, idx_1_not_in_2, idx_2_not_in_1 = process_curry(df_1, df_2)
    else:
        return render_template("index_1.html")

    output = {"columns in file 1 but not in file 2": col_1, "columns in file 2 but not in file 1": col_2, "devices not in file 2": [missing_dv_1], "devices not in file 1": [
        missing_dv_2], "indices not in file 1": [idx_2_not_in_1], "indices not in file 2": [idx_1_not_in_2], "mis matched values": [disc]}
    #print(output)
    return render_template("index_1.html", dataFromFlask=json.dumps(output))

###
# Main Driver Function
if __name__ == "__main__":
    # Run the application on the local development server
    app.run(debug=True)
