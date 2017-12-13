def already_submitted(request, data):
    """Returns whether the data have already been submitted."""
    if 'forbidden_data' not in request.session:
        request.session['forbidden_data'] = []

    hashed = hash(data)
    if hashed not in request.session['forbidden_data']:
        request.session['forbidden_data'].append(hashed)
        return False
    return True


def get_choice(course, constructor, user=None):
    """Given a Course and a form constructor, return the Course's choice index."""
    form = constructor(user=user if user else course.user)
    for choice in form.fields['course'].choices:
        if choice[1] == course.name:
            return choice[0]
