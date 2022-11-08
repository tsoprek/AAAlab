from django.views.generic import TemplateView
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.template import Template
from scripts.applications import Radius_Cfg
from scripts.ResetConfigISE import Reset_Cfg_ISE
from scripts.rm_aaa import ConnectToDevice, rm_AAA

def BasePage(request):
    return render(request, 'base.html')

def HomePage(request):
        return render (request, 'home.html')

def RadiusPage(request):

    if request.method == 'GET':
        return render (request, 'radius.html')

    elif request.method == 'POST':

        server_list= []
        dev_list= []

        # Get servers and add to list
        server_list.append(request.POST['server1'])
        server_list.append(request.POST['server2'])
        server_list.append(request.POST['server3'])

        # Get NAD devices and create list
        devices= request.POST['device-list']
        for dev in devices.replace(" ", "").split(','):
            dev_list.append(dev)

        # Get VRF adn source interfaces
        vrf=request.POST['vrf']
        source_if = request.POST['source-if']
        dot1x_if = request.POST['dot1x-if']

        # Run radius application
        context= Radius_Cfg(dev_list, server_list, vrf, source_if, dot1x_if)
        context=(str(context)).split('\n')
        print(type(context))
        # Additional options
        ssh = request.POST['ssh-cfg']
        tacacs = request.POST['tacacs']
        rm_aaa = request.POST['rm-aaa']

        return render(request, 'success.html', { 'context': context } )


def TacacsPage(request):

    if request.method == 'GET':
        return render (request, 'tacacs.html')

    elif request.method == 'POST':
        dev_list= []
        devices= request.POST['device-list']
        ssh = request.POST['ssh-cfg']
        radius = request.POST['radius']
        rm_aaa = request.POST['rm-aaa']
        for dev in devices.replace(" ", "").split(','):
            dev_list.append(dev)
        #if rm_aaa == 'yes':
            #need to get switch defaults script
        #    continue
        #else:
        #    continue
        if radius == 'yes':
            file= '/config_templates/radius_generic'
            configuration = read_file(file)
            for device in dev_list:
               conn = connect_to_device(device)
               configure_device(conn, configuration)
        for device in dev_list:
            file= '../config_templates/TACACSConfig'
            configuration = read_file(file)
            conn = connect_to_device(device)
            context = configure_device(conn, configuration)
            print ('')
            return render(request, 'tacacs.html', { 'context':context } )

def SGTPage(request):

    if request.method == 'GET':
        return render (request, 'sgt.html')

    elif request.method == 'POST':
        dev_list= []
        devices= request.POST['device-list']
        ssh = request.POST['ssh-cfg']
        radius = request.POST['radius']
        rm_aaa = request.POST['rm-aaa']
        for dev in devices.replace(" ", "").split(','):
            dev_list.append(dev)
        if rm_aaa == 'yes':
            file='scripts/rm_aaa'
        #    continue
        #else:
        #    continue
        if radius == 'yes':
            file= '/config_templates/radius_generic'
            configuration = read_file(file)
            for device in dev_list:
               conn = connect_to_device(device)
               configure_device(conn, configuration)
        for device in dev_list:
            file= '/config_templates/TACACSConfig'
            configuration = read_file(file)
            conn = connect_to_device(device)
            context = configure_device(conn, configuration)
            print ('')
            return render(request, 'tacacs.html', {'context':context} )

def SuccessPage(request):
    return render(request, 'success.html', {'context':context})

def Reset_config_ISE_page(request):
    if request.method == 'GET':
        return render (request, 'rst_cfg_ise.html')

    elif request.method == 'POST':
        dev_list= []

        # Get NAD devices and create list
        devices= request.POST['device-list']
        for dev in devices.replace(" ", "").split(','):
            dev_list.append(dev)
        #Run application
        Reset_Cfg_ISE(dev_list)
        return render(request, 'rst_cfg_ise.html')

def Rm_Aaa(request):
    if request.method == 'GET':
        return render (request, 'rm_aaa.html')

    elif request == 'POST':
        dev_list = []

        # Get NAD devices and create list
        devices = request.POST['device-list']
        for dev in devices.replace(" ", "").split(','):
            print(dev)
            connection = ConnectToDevice(dev)
            rm_AAA(connection)
        return render(request, 'rm_aaa.html')
