from .models import SubCategory, SuperCategory


def tshop_context_processor(request):
    context = {}
    context["super_categories"] = SuperCategory.objects.all()
    context["sub_categories"] = SubCategory.objects.all()
    return context
