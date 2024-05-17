from django.urls import path

from statements.views.statement import (StatementCreateFreeAPIView,
                                        StatementCreateGroupAPIView,
                                        StatementCreateEventAPIView,
                                        StatementDownloadAPIView)

urlpatterns = [
    path("free/", StatementCreateFreeAPIView.as_view(), name="statement-create-free"),
    path("group/", StatementCreateGroupAPIView.as_view(), name="statement-create-group"),
    path("event/", StatementCreateEventAPIView.as_view(), name="statement-create-event"),
    path("<int:id>/download/", StatementDownloadAPIView.as_view(), name="statement-download"),
]
