import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_retrieve_course(api_client, course_factory):
    """Проверка получения первого курса (retrieve-логика)"""
    course = course_factory('students.Course')
    url = reverse('courses-detail', kwargs={'pk': course.id})

    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name

def test_list_courses(api_client, course_factory):
    """Проверка получения списка курсов (list-логика)"""
    course_factory('students.Course', _quantity=3)
    url = reverse('courses-list')

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3

def test_filter_courses_by_id(api_client, course_factory):
    """Проверка фильтрации списка курсов по id"""
    course1 = course_factory('students.Course')
    course2 = course_factory('students.Course')
    url = reverse('courses-list')

    # Передаем GET-параметр через data
    response = api_client.get(url, data={'id': course1.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id

def test_filter_courses_by_name(api_client, course_factory):
    """Проверка фильтрации списка курсов по name"""
    unique_name = "Уникальный курс по Python"
    course1 = course_factory('students.Course', name=unique_name)
    course_factory('students.Course', name="Другой курс")
    url = reverse('courses-list')

    response = api_client.get(url, data={'name': unique_name})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == unique_name

def test_create_course_success(api_client):
    """Тест успешного создания курса"""
    url = reverse('courses-list')
    data = {
        'name': 'Новый курс',
        'description': 'Описание нового курса'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['name'] == 'Новый курс'

def test_update_course_success(api_client, course_factory):
    """Тест успешного обновления курса"""
    course = course_factory('students.Course', name='Старое название')
    url = reverse('courses-detail', kwargs={'pk': course.id})
    data = {'name': 'Обновленное название'}

    response = api_client.patch(url, data, format='json') # или put, в зависимости от вашей реализации

    assert response.status_code == 200
    assert response.data['name'] == 'Обновленное название'

def test_delete_course_success(api_client, course_factory):
    """Тест успешного удаления курса"""
    course = course_factory('students.Course')
    url = reverse('courses-detail', kwargs={'pk': course.id})

    response = api_client.delete(url)

    assert response.status_code == 204

    @pytest.mark.parametrize("students_count, expected_status", [
        (2, 200),  # Успех: количество равно лимиту (лимит переопределен до 2)
        (3, 400),  # Ошибка: количество превышает лимит
    ])
def test_max_students_per_course_validation(
        api_client, course_factory, student_factory, settings, students_count, expected_status
):
    """
    Тест ограничения числа студентов на курсе.
    Мы переопределяем настройку MAX_STUDENTS_PER_COURSE до 2,
    чтобы не создавать 20 сущностей в БД для проверки ошибки.
    """
    # Переопределяем настройку Django только для этого теста
    settings.MAX_STUDENTS_PER_COURSE = 2

    course = course_factory('students.Course')
    students = student_factory('students.Student', _quantity=students_count)
    student_ids = [student.id for student in students]

    url = reverse('courses-detail', kwargs={'pk': course.id})

    # Предполагаем, что ваш API принимает список ID студентов при обновлении курса
    data = {'students': student_ids}

    response = api_client.patch(url, data, format='json')

    assert response.status_code == expected_status
    if expected_status == 400:
        assert 'students' in response.data or 'non_field_errors' in response.data
