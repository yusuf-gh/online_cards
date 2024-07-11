from django.shortcuts import render
import templates


def main_page(request):
    return render(request, '../templates/base.html')
