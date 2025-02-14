from setuptools import setup, find_packages

setup(
    name="GenAIAudit",
    version="0.1",
    py_modules=["gen_audit"],  # Change this if your script has a different name
    install_requires=[],  # Add any dependencies
    entry_points={
        "console_scripts": [
            "GenAIAudit=gen_audit:main"
        ],
    },
)
