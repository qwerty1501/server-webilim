

def get_membership(user, course):
    try:
        user.user_membership.register_request
        compounds = [compound.course for compound in user.user_membership.register_request.package_membership.base_compound.all()]
        print(compounds)
    except:
        return False
    else:
        print(course)
        if course in compounds:
            return True
        else:
            return False
