from django.shortcuts import render

# Create your views here.
# from django.contrib.auth.decorators import login_required

# @login_required
def charts(request):
    return render(request, "chart_test.html")

# @login_required
def pulse_chart(request, device):
    device = device.capitalize()
    # print("DEVICE:",device)
    return render(request, "charts.html", {'device': device})

# @login_required
def all_pulse_charts(request):
    return render(request, "charts_all.html", {'device': "All Pulse"})

def temp_chart(request, device):
    device = device.capitalize()
    # print("DEVICE:",device)
    return render(request, "temp_chart.html", {'device': device})