from flask import Flask, render_template, request
import pickle
import numpy as np

# Setup application
app = Flask(__name__)

def prediction(lst):
    filename = 'model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([lst])
    return pred_value

@app.route('/', methods=['POST', 'GET'])
def index():
    pred_value = 0
    input_data = {  # Initialize the input data dictionary
        "ram": "",
        "weight": "",
        "company": "",
        "typename": "",
        "opsys": "",
        "cpuname": "",
        "gpuname": "",
        "touchscreen": [],
        "ips": []
    }

    if request.method == 'POST':
        # Collect the input values
        input_data['ram'] = request.form['ram']
        input_data['weight'] = request.form['weight']
        input_data['company'] = request.form['company']
        input_data['typename'] = request.form['typename']
        input_data['opsys'] = request.form['opsys']
        input_data['cpuname'] = request.form['cpuname']
        input_data['gpuname'] = request.form['gpuname']
        input_data['touchscreen'] = request.form.getlist('touchscreen')
        input_data['ips'] = request.form.getlist('ips')

        feature_list = []

        feature_list.append(int(input_data['ram']))
        feature_list.append(float(input_data['weight']))
        feature_list.append(len(input_data['touchscreen']))
        feature_list.append(len(input_data['ips']))

        company_list = ['acer', 'apple', 'asus', 'dell', 'hp', 'lenovo', 'msi', 'other', 'toshiba']
        typename_list = ['2in1convertible', 'gaming', 'netbook', 'notebook', 'ultrabook', 'workstation']
        opsys_list = ['linux', 'mac', 'other', 'windows']
        cpu_list = ['amd', 'intelcorei3', 'intelcorei5', 'intelcorei7', 'other']
        gpu_list = ['amd', 'intel', 'nvidia']

        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)

        traverse_list(company_list, input_data['company'])
        traverse_list(typename_list, input_data['typename'])
        traverse_list(opsys_list, input_data['opsys'])
        traverse_list(cpu_list, input_data['cpuname'])
        traverse_list(gpu_list, input_data['gpuname'])

        pred_value = prediction(feature_list)
        pred_value = np.round(pred_value[0], 2) * 305

    return render_template('index.html', pred_value=pred_value, input_data=input_data)


if __name__ == '__main__':
    app.run(debug=True)
