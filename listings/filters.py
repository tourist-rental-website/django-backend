import django_filters
from .models import GuideProfile


class GuideProfileFilter(django_filters.FilterSet):

    min_experience = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="gte"
    )

    max_experience = django_filters.NumberFilter(
        field_name="experience_years",
        lookup_expr="lte"
    )
    location = django_filters.CharFilter(
    field_name="location",
    lookup_expr="iexact"
    )

    class Meta:
        model = GuideProfile
        fields = []