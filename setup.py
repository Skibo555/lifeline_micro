from setuptools import setup, find_packages

setup(
    name="rabbitmq_service",
    version="0.1",
    packages=find_packages(),
    install_requires=["aio_pika"],
)