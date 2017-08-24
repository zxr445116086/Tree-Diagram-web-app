from flask import Flask, render_template, request, redirect, url_for
import json
from xml.dom import minidom
import os
from subprocess import call
from copy import deepcopy

app = Flask(__name__)



@app.route('/')
@app.route('/duikang/')
def duikang():
    return render_template('tuopu5.html')

@app.route('/tuopu/')
def tuopu():
    return render_template('tuopu2.html')

@app.route('/process', methods=['POST'])
def process():
    content = request.form.get('tuopuData')
    content = json.loads(content,encoding="UTF-8")
    data = content["nodeDataArray"]

    for item in data:
        if 'Name' not in item.keys():
            item["Name"] = "new_Device"

    for item in data:
        if 'parameter1' not in item.keys():
            item["parameter1"] = "parameter1"

    root = minidom.Document()
    contest = root.createElement('contest')
    root.appendChild(contest)

    topChild = root.createElement("networktopology")
    contest.appendChild(topChild)

    vpcChild = root.createElement("vpcnetworks")
    topChild.appendChild(vpcChild)
    vnChild = root.createElement("networks")
    topChild.appendChild(vnChild)
    vmChild = root.createElement("virtualmachines")
    topChild.appendChild(vmChild)




    rootKey = ''

    # 生成vpcnetwork节点
    for item in data:
        if 'parent' not in item.keys():
            rootKey = str(item["key"])
            vpcSecondChild = root.createElement("vpcnetwork")
            vpcChild.appendChild(vpcSecondChild)
            vpcParameter1 = root.createElement("name")
            vpcParameter1.appendChild(root.createTextNode(item["Name"]))
            vpcSecondChild.appendChild(vpcParameter1)
            vpcParameter2 = root.createElement("cidr")
            vpcParameter2.appendChild(root.createTextNode(item["parameter1"]))
            vpcSecondChild.appendChild(vpcParameter2)
            break

    for item in data:
        if 'parent' in item.keys():
            if str(item["parent"]) == rootKey:
                vnSecondChild = root.createElement("network")
                vnChild.appendChild(vnSecondChild)
                vnParameter1 = root.createElement("name")
                vnParameter1.appendChild(root.createTextNode(item["Name"]))
                vnSecondChild.appendChild(vnParameter1)
                vnParameter2 = root.createElement("gateway")
                vnParameter2.appendChild(root.createTextNode(item["parameter1"]))
                vnSecondChild.appendChild(vnParameter2)
                vnParameter3 = root.createElement("netmask")
                vnParameter3.appendChild(root.createTextNode(item["parameter2"]))
                vnSecondChild.appendChild(vnParameter3)
                vnParameter4 = root.createElement("vpcid")
                vnParameter4.appendChild(root.createTextNode([i["Name"] for i in data if str(i["key"]) == rootKey][0]))
                vnSecondChild.appendChild(vnParameter4)

    for item in data:
        if 'parent' in item.keys():
            if str(item["parent"]) != rootKey:
                vmSecondChild = root.createElement("virtualmachine")
                vmChild.appendChild(vmSecondChild)
                vmParameter1 = root.createElement("name")
                vmParameter1.appendChild(root.createTextNode(item["Name"]))
                vmSecondChild.appendChild(vmParameter1)
                vmParameter2 = root.createElement("networkids")
                vmParameter2.appendChild(root.createTextNode([i["Name"] for i in data if str(i["key"]) == str(item["parent"])][0]))
                vmSecondChild.appendChild(vmParameter2)
                vmParameter3 = root.createElement("serviceofferingid")
                vmParameter3.appendChild(root.createTextNode(item["parameter1"]))
                vmSecondChild.appendChild(vmParameter3)
                vmParameter4 = root.createElement("templateid")
                vmParameter4.appendChild(root.createTextNode(item["parameter2"]))
                vmSecondChild.appendChild(vmParameter4)


    xml_str = root.toprettyxml(indent="\t",encoding="UTF-8")

    save_path_file = "tuopu.xml"
    with open(save_path_file, "wb") as f:
        f.write(xml_str)

    return "finish"

@app.route('/dksc', methods=['POST'])
def dksc():
    num = request.form.get('tuopuNum')
    num = int(num)
    content = request.form.get('tuopuData')
    content = json.loads(content, encoding="UTF-8")
    data = content["nodeDataArray"]

    for item in data:
        if 'Name' not in item.keys():
            item["Name"] = "new_Device"

    for item in data:
        if 'parameter1' not in item.keys():
            item["parameter1"] = "parameter1"

    root = minidom.Document()
    contest = root.createElement('contest')
    root.appendChild(contest)

    topChild = root.createElement("networktopology")
    contest.appendChild(topChild)

    vpcChild = root.createElement("vpcnetworks")
    topChild.appendChild(vpcChild)
    vnChild = root.createElement("networks")
    topChild.appendChild(vnChild)
    vmChild = root.createElement("virtualmachines")
    topChild.appendChild(vmChild)

    dataList = []
    n = 0

    for i in range(num):
        rootKey = ''
        dataCopy = deepcopy(data)
        for item in dataCopy:
            if 'parent' not in item.keys():
                rootKey = str(item["key"])
                item["parameter1"] = '.'.join((item["parameter1"].split('.')[0],item["parameter1"].split('.')[1],str(int(item["parameter1"].split('.')[2]) + i),item["parameter1"].split('.')[3]))
                item["Name"] = item["Name"] + '_' + str(i+1)

        minNetmask = 1000
        for item in dataCopy:
            if 'parent' in item.keys():
                if str(item["parent"]) == rootKey:
                    if int(item["parameter1"].split('.')[2]) <= minNetmask:
                        minNetmask = int(item["parameter1"].split('.')[2])

        for item in dataCopy:
            if 'parent' in item.keys():
                if str(item["parent"]) == rootKey:
                    item["Name"] = item["Name"] + '_' + str(i+1)
                    item["parameter1"] = '.'.join((item["parameter1"].split('.')[0],item["parameter1"].split('.')[1],str(minNetmask + n),item["parameter1"].split('.')[3]))
                    n += 1
                    #item["parameter2"] = [i["Name"] for i in dataCopy if str(i["key"]) == rootKey][0]

        for item in dataCopy:
            if 'parent' in item.keys():
                if str(item["parent"]) != rootKey:
                    item["Name"] = item["Name"] + '_' + str(i+1)

        dataList.append(dataCopy)


    for dataItem in dataList:

        rootKey = ''

        # 生成vpcnetwork节点
        for item in dataItem:
            if 'parent' not in item.keys():
                rootKey = str(item["key"])
                vpcSecondChild = root.createElement("vpcnetwork")
                vpcChild.appendChild(vpcSecondChild)
                vpcParameter1 = root.createElement("name")
                vpcParameter1.appendChild(root.createTextNode(item["Name"]))
                vpcSecondChild.appendChild(vpcParameter1)
                vpcParameter2 = root.createElement("cidr")
                vpcParameter2.appendChild(root.createTextNode(item["parameter1"]))
                vpcSecondChild.appendChild(vpcParameter2)
                break

        for item in dataItem:
            if 'parent' in item.keys():
                if str(item["parent"]) == rootKey:
                    vnSecondChild = root.createElement("network")
                    vnChild.appendChild(vnSecondChild)
                    vnParameter1 = root.createElement("name")
                    vnParameter1.appendChild(root.createTextNode(item["Name"]))
                    vnSecondChild.appendChild(vnParameter1)
                    vnParameter2 = root.createElement("gateway")
                    vnParameter2.appendChild(root.createTextNode(item["parameter1"]))
                    vnSecondChild.appendChild(vnParameter2)
                    vnParameter3 = root.createElement("netmask")
                    vnParameter3.appendChild(root.createTextNode(item["parameter2"]))
                    vnSecondChild.appendChild(vnParameter3)
                    vnParameter4 = root.createElement("vpcid")
                    vnParameter4.appendChild(root.createTextNode([i["Name"] for i in dataItem if str(i["key"]) == rootKey][0]))
                    vnSecondChild.appendChild(vnParameter4)

        for item in dataItem:
            if 'parent' in item.keys():
                if str(item["parent"]) != rootKey:
                    vmSecondChild = root.createElement("virtualmachine")
                    vmChild.appendChild(vmSecondChild)
                    vmParameter1 = root.createElement("name")
                    vmParameter1.appendChild(root.createTextNode(item["Name"]))
                    vmSecondChild.appendChild(vmParameter1)
                    vmParameter2 = root.createElement("networkids")
                    vmParameter2.appendChild(root.createTextNode([i["Name"] for i in dataItem if str(i["key"]) == str(item["parent"])][0]))
                    vmSecondChild.appendChild(vmParameter2)
                    vmParameter3 = root.createElement("serviceofferingid")
                    vmParameter3.appendChild(root.createTextNode(item["parameter1"]))
                    vmSecondChild.appendChild(vmParameter3)
                    vmParameter4 = root.createElement("templateid")
                    vmParameter4.appendChild(root.createTextNode(item["parameter2"]))
                    vmSecondChild.appendChild(vmParameter4)


    xml_str = root.toprettyxml(indent="\t",encoding="UTF-8")

    save_path_file = "tuopu.xml"
    with open(save_path_file, "wb") as f:
        f.write(xml_str)

    return "finish"

@app.route('/confirm', methods=['GET','POST'])
def confirm():
    if request.method == 'GET':
        with open('tuopu.xml', "r") as f:
            xml_str = f.read()
        return render_template('confirm.html', xmlString=xml_str)
    else:
        content = request.form.get('confirmData')
        if content == "go":
            call(["ls", "-l"])
        return "finish"
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8010)