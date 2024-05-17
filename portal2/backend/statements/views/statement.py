
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from statements.models.statement import Statement
from statements.serializers.statement import GroupStatementSerializer, \
    FreeStatementSerializer, EventStatementSerializer, \
    DownloadStatementSerializer


class StatementCreateFreeAPIView(CreateAPIView):
    serializer_class = FreeStatementSerializer
    queryset = Statement.objects.all()


class StatementCreateGroupAPIView(CreateAPIView):
    serializer_class = GroupStatementSerializer
    queryset = Statement.objects.all()


class StatementCreateEventAPIView(CreateAPIView):
    serializer_class = EventStatementSerializer
    queryset = Statement.objects.all()


class StatementDownloadAPIView(RetrieveAPIView):
    serializer_class = DownloadStatementSerializer
    queryset = Statement.objects.all()
    lookup_field = "id"
