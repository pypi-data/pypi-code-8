from distutils.core import setup

setup(
        name             = "odoo-ook",
        version          = "5.0.7",
        author           = "Frederic van der Essen",
        author_email     = "fvdessen+x@gmail.com",
        packages         = ["ook"],
        url              = "https://github.com/fvdsn/odoo-ook",
        license          = "MIT",
        install_requires = [
            "appdirs",
            "flake"
        ],
        scripts          = [
            "scripts/ook"
        ]
    )

