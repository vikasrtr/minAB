"""
minAB

Minimalist A/b testing framework for python

__author__: vikas_rtr

"""

from flask import Flask, render_template, request, jsonify
import uuid

import sys
sys.path.append('../../minAB')

from minab.experiments import ABExperiment

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def homepage():

    # start an experiment for conversion
    my_exp = ABExperiment()

    # create an A/B test
    user = str(uuid.uuid4())
    btn_class = my_exp.ab_test(
        'signup_button_color', user, 'conv_button_a', 'conv_button_b')

    if request.method == 'GET':
        try:
            return render_template('index.html', btn_class=btn_class, user=user)
        except:
            return sys.exc_info()

    elif request.method == 'POST':

        # log a successful conversion
        last_user = request.form.get('user_id')
        old_btn_class = request.form.get('exp_value')
        my_exp.finished('signup_button_color', last_user, old_btn_class)

        try:
            return render_template('index.html', btn_class=btn_class, user=user)
        except:
            return sys.exc_info()


@app.route('/data', methods=['POST'])
def data_download():
    exp = ABExperiment()
    exp_data, exp_conversion = exp.get_data()

    try:
        return render_template('data.html', exp_data=exp_data, exp_conversion=exp_conversion)
    except:
        return sys.exc_info()

if __name__ == "__main__":
    app.debug = True
    app.run()
