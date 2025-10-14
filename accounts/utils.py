from .models import UserDepartmentRight
from utils.templatetags.rights import has_dept_right as _has, has_any_dept_rights as _has_any

# def has_department_right(user, department, right_code: str, module: str = "core") -> bool:
#     return UserDepartmentRight.objects.filter(
#         user=user,
#         department=department,
#         right__name__iexact=right_code,
#         right__module__iexact=module
#     ).exists()
def has_department_right(user, department, right_code: str, module: str = "requests") -> bool:
    return _has(department, right_code, user, module)

def has_any_department_rights(user, department, right_codes, module: str = "requests") -> bool:
    return _has_any(department, right_codes, user, module)