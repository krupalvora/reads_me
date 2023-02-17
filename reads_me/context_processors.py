from reads_me.constants import CATEGORIES


def add_context(request):
    context = {
        "categories": CATEGORIES
    }
    return context