import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

from rest_framework_simplejwt.tokens import RefreshToken

from django.db.models import F,Count,Case,IntegerField,When,Value,ExpressionWrapper,CharField
from django.db import models
from django.utils import timezone

from .models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



def get_age_group():
    today = timezone.now().date()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    raw_age_expression = ExpressionWrapper(
        current_year - F('dob__year'),
        output_field=IntegerField()
    )

    adjusted_age_expression = ExpressionWrapper(
        raw_age_expression - Case(
            When(
                dob__month__gt=current_month,
                then=Value(1)
            ),
            When(
                dob__month=current_month,
                dob__day__gt=current_day,
                then=Value(1)
            ),
            default=Value(0),
            output_field=IntegerField()
        ),
        output_field=IntegerField()
    )

    age_groups = User.objects.annotate(
        age=adjusted_age_expression
    ).annotate(
        age_group=Case(
            When(age__lte=20, then=Value('1-20')),
            When(age__lte=40, then=Value('20-40')),
            default=Value('40+'),
            output_field=CharField()
        )
    ).values('age_group').annotate(count=Count('id')).order_by('age_group')

    age_group_dict = {
        '1-20': 0,
        '20-40': 0,
        '40+': 0
    }
    for group in age_groups:
        age_group_dict[group['age_group']] = group['count']

    return age_group_dict



def plot_age_groups():
    age_groups = get_age_group()
    groups = list(age_groups.keys())
    counts = list(age_groups.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(groups, counts, color=['skyblue', 'orange', 'lightgreen'])
    ax.set_xlabel('Age Group')
    ax.set_ylabel('Number of Users')
    ax.set_title('Number of Users in Each Age Group')


    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return img_base64
