from .forms import CustomUserCreationForm, LoginForm
from .models import CustomUser, FriendRequest
from .serializers import FriendRequestSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout 
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions, filters

# Create your views here.

# Home page
def index(request):
    return render(request, 'index.html')

# signup page
def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user) 
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


# def friend_request(request, email):
#     user = CustomUser.objects.filter(email=email)
#     if user and user != request.user:
#         FriendRequest.objects.create(status=False, to_user = user.first(), from_user=request.user)
#     return HttpResponse(f'<h3>Friend Request sent to {email} </h3>')

class UserAPIView(generics.ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """
    search_fields  = ['first_name', 'last_name', 'email']
    filter_backends = (filters.SearchFilter,)    
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# users/views.py
class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        to_user_id = self.request.data.get('to_user')
        to_user = CustomUser.objects.filter(id=to_user_id).first()
        serializer.save(from_user=self.request.user, to_user=to_user)

class FriendRequestPendingView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return  self.queryset.filter(status=False, to_user=self.request.user)

class FriendsView(generics.ListAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return  self.queryset.filter(status=True, to_user=self.request.user)

class FriendRequestAcceptView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        from_user = CustomUser.objects.filter(pk=self.kwargs['pk']).first()
        instance = FriendRequest.objects.filter(status=False, to_user=self.request.user, from_user=from_user)
        if instance:
            instance = instance.first()
            if instance.to_user_id != request.user.id:
                return Response({"detail": "You can only accept requests sent to you."}, status=status.HTTP_403_FORBIDDEN)
            instance.status = True
            instance.save()
            return Response(FriendRequestSerializer(instance).data)
        return Response({"detail": "You are already a friend or No user exists."})

    # def delete(self, request, *args, **kwargs):
    #     return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return FriendRequest.objects.filter(status=False, to_user=self.request.user)
