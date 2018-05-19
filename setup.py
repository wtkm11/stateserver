from setuptools import setup

setup(
    name="StateServer",
    version="1.0",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    install_requires=[
        "falcon",
        "gunicorn",
        "rtree",
        "shapely[vectorized]"
    ]
)
