
from user.models import UserInformation
from .modelSerializer import ReviewManuscriptSerializer,ManuscriptSerializer

class ReviewPermission(object):

    def __init__(self,request,permission):
        self._request=request
        self._permission=permission

    def selectManuscript(self):
        _username=self._request.user
        if _username.has_perm(self._permission):
            pass


