from django.db.models import Q
from backend.accounts.models import Friendship
from django.contrib.auth.models import User

def get_friends(user: User):
    friendships = Friendship.objects.filter(
        Q(from_user=user, accepted=True) | Q(to_user=user, accepted=True)
    )
    return [f.to_user if f.from_user == user else f.from_user for f in friendships]

def get_pending_sent_requests(user: User):
    return Friendship.objects.filter(from_user=user, accepted=False)

def get_pending_received_requests(user: User):
    return Friendship.objects.filter(to_user=user, accepted=False)

def is_friend_with(user1: User, user2: User):
    return Friendship.objects.filter(
        Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1),
        accepted=True
    ).exists()

def has_pending_request(user1: User, user2: User):
    return Friendship.objects.filter(
        Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1),
        accepted=False
    ).exists()
