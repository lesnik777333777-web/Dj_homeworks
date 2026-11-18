import pytest
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def api_client():
    """Фикстура для API клиента DRF"""
    return APIClient()

@pytest.fixture
def course_factory():
    """Фикстура фабрики для создания курсов"""
    return baker.make

@pytest.fixture
def student_factory():
    """Фикстура фабрики для создания студентов"""
    return baker.make