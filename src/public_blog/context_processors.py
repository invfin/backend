def keep_email(request):
    email = ""
    try:
        if request.user.is_anonymous:
            try:
                email = request.session["F-E"]
            except Exception:
                email = email

        return {"anon_email": email}
    except Exception:
        pass
    return {}
