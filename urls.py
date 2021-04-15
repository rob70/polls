from django.urls import path

from . import views 

app_name = 'polls'
urlpatterns = [
# ex: /polls/
    path('', views.pollviews.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.pollviews.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.pollviews.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.pollviews.vote, name='vote'),
    # category
    path('category/<int:question_category_id>/', views.pollviews.categorydetails, name='categorydetails'),
    path('category/edit/<int:question_category_id>/', views.pollviews.manage_questions, name='manage_questions'),
    path('category/results/<int:question_category_id>/', views.pollviews.category_results, name='cat_results'),
    path("surveys/<int:question_category_id>/", views.pollviews.submit, name="survey-submit"),
    path('mypage', views.pollviews.student_overview, name="min-side"),
    path("signup/", views.auth.register, name="register"),
    path("login/", views.auth.logg_inn, name="login"),
    path("logout/", views.auth.logout, name="logged-out"),
]