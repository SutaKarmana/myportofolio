from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Award, Project
from main.permissions import (
    IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly,
)
from main.serializers import AwardQuerySerializer, AwardSerializer, ProjectSerializer

@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        serializer = ProjectSerializer(
            projects, many=True, context={"request": request},
        )
        return Response(serializer.data)

    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related("starred_by"), pk=project_id,
    )
    if request.method in ("GET", "HEAD"):
        serializer = ProjectSerializer(project, context={"request": request})
        return Response(serializer.data)

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProjectSerializer(
        project, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    serializer = ProjectSerializer(project, context={"request": request})
    return Response(serializer.data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def award_list(request):
    if request.method in ("GET", "HEAD"):
        query = AwardQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        filters = query.validated_data
        # Pola Tutorial 07: ambil relasi sekali untuk seluruh kartu, hindari N+1.
        awards = Award.objects.prefetch_related("liked_by")
        if filters["q"]:
            awards = awards.filter(title__icontains=filters["q"])
        if "year" in filters:
            awards = awards.filter(year=filters["year"])
        # Whitelist mencegah field arbitrer dipakai untuk pengurutan.
        ordering = {
            "-year": ("-year", "title", "id"),
            "year": ("year", "title", "id"),
            "title": ("title", "-year", "id"),
        }
        awards = awards.order_by(*ordering[filters["ordering"]])
        return Response(AwardSerializer(
            awards, many=True, context={"request": request},
        ).data)

    serializer = AwardSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def award_detail(request, award_id):
    award = get_object_or_404(Award.objects.prefetch_related("liked_by"), pk=award_id)
    if request.method in ("GET", "HEAD"):
        return Response(AwardSerializer(award, context={"request": request}).data)
    if request.method == "DELETE":
        award.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = AwardSerializer(
        award, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def award_star(request, award_id):
    """Toggle Like memakai akun session, tidak menerima ID pemberi dari payload."""
    award = get_object_or_404(Award, pk=award_id)
    if award.liked_by.filter(pk=request.user.pk).exists():
        award.liked_by.remove(request.user)
    else:
        award.liked_by.add(request.user)
    return Response(AwardSerializer(award, context={"request": request}).data)
