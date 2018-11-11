from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login,logout
from ssh.models import LoginInfo
from django.shortcuts import redirect
from ipware import get_client_ip
PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
  
def get_client_ip(request):
    """get the client ip from the request
    """
    remote_address = request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        # take the first ip which is not a private one (of a proxy)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip
def index(request):
    aa = get_client_ip(request)
    return render(request, 'home.html',{'ip':aa,})

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request,user)
                LoginInfo.objects.create(user=user, ip=get_client_ip(request))
                return redirect('/')
        else:
        	return HttpResponse('fail')
    
    else:
    	loginrForm = LoginForm() 
    	return render(request, 'login.html', {'form':loginrForm})

def logoutUser(request):
    logout(request)
    return redirect('/login')