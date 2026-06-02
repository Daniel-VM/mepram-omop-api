from core import models
from core.api.services import db
from drf_spectacular.views import SpectacularAPIView


CAPABILITIES = {
    "supports_clinical_aggregates": True,
    "supports_age_stratification": True,
    "supports_sex_stratification": True,
    "supports_numeric_measurements": True,
    "supports_categorical_measurements": True,
    "supports_isolate_explorer": False,
    "supports_genomic_alerts": False,
}


def metadata_summary(request=None):
    event_types = db.rows(
        models.FactConcept.objects.values("event_type")
        .distinct()
        .order_by("event_type")
    )
    domains = db.rows(
        models.FactDomain.objects.values(
            "domain_id", "medical_concepts", "participants"
        ).order_by("-participants", "domain_id")
    )
    age_groups = db.rows(
        models.DimPatient.objects.exclude(age_group__isnull=True)
        .values("age_group")
        .distinct()
        .order_by("age_group")
    )
    genders = db.rows(
        models.DimPatient.objects.exclude(gender__isnull=True)
        .values("gender")
        .distinct()
        .order_by("gender")
    )
    vocabularies = db.rows(
        models.Concept.objects.exclude(vocabulary_id__isnull=True)
        .values("vocabulary_id")
        .distinct()
        .order_by("vocabulary_id")
    )
    openapi = None
    if request is not None:
        try:
            resp = SpectacularAPIView().get(request)
            openapi = resp.data
        except Exception:
            openapi = None

    return {
        "schema": db.dashboard_schema(),
        "openapi": openapi,
        "domains": domains,
        "event_types": [row["event_type"] for row in event_types],
        "age_groups": [row["age_group"] for row in age_groups],
        "genders": [row["gender"] for row in genders],
        "vocabularies": [row["vocabulary_id"] for row in vocabularies],
        "total_patients": models.DimPatient.objects.count(),
        "capabilities": capabilities(),
    }


def capabilities():
    return dict(CAPABILITIES)
