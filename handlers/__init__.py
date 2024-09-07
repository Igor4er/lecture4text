import pkgutil

handlers_list = [
    name for _, name, _ in pkgutil.iter_modules(__path__)
    if not name.startswith('_')
]
# I would like to say thanks to PWZER/swagger-ui-py
