from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Task, User
from .serializers import TaskSerializer


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # List tasks created by or assigned to the logged-in user
    def get(self, request):
        tasks = Task.objects.filter(
            Q(created_by=request.user) |
            Q(assigned_to=request.user)
        )

        # Filter by status
        task_status = request.query_params.get("status")
        if task_status:
            tasks = tasks.filter(status=task_status)

        # Filter by assigned user ID
        assigned_to = request.query_params.get("assigned_to")
        if assigned_to:
            tasks = tasks.filter(assigned_to_id=assigned_to)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # Create task
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = serializer.save(
            created_by=request.user,
            status="open",
        )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_201_CREATED,
        )


class AssignTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Creator can assign or reassign
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if task.created_by_id != request.user.id:
            return Response(
                {"error": "Only the creator can assign or reassign"},
                status=status.HTTP_403_FORBIDDEN,
            )

        assigned_to_id = request.data.get("assigned_to")

        if not assigned_to_id:
            return Response(
                {"error": "assigned_to is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            assigned_user = User.objects.get(pk=assigned_to_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Invalid assigned user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not assigned_user.is_active:
            return Response(
                {"error": "Cannot assign task to an inactive user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        task.assigned_to = assigned_user
        task.save(update_fields=["assigned_to", "updated_at"])

        return Response(TaskSerializer(task).data)


class TaskStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # Creator or assigned user can change status
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if (
            task.created_by_id != request.user.id
            and task.assigned_to_id != request.user.id
        ):
            return Response(
                {"error": "Only the creator or assigned user can change status"},
                status=status.HTTP_403_FORBIDDEN,
            )

        new_status = request.data.get("status")

        if not new_status:
            return Response(
                {"error": "status is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_statuses = ["open", "in_progress", "done"]

        if new_status not in valid_statuses:
            return Response(
                {"error": "Invalid status"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            task.change_status(new_status)
        except ValueError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(TaskSerializer(task).data)