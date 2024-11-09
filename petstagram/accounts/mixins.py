def optional_field(**kwargs):
    kwargs["blank"] = kwargs.get("blank", True)
    kwargs["null"] = kwargs.get("null", True)

    return kwargs

