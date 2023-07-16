from setuptools import find_packages, setup


def get_long_description():
    with open("README.md") as file:
        return file.read()


setup(
    name="EyeTrackFatigue",
    version="0.2.1",
    description="EyeTrackFatigue description",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="...",
    author_email="anton.mamonov.golohvastogo@mail.ru",
    url="https://github.com/AI-group-72/FAEyeTON",
    project_urls={
        "GitHub Project": "https://github.com/AI-group-72/FAEyeTON",
        "Issue Tracker": "https://github.com/AI-group-72/FAEyeTON/Meta/issues",
    },
    packages=find_packages(
        include=["DeviceManager", "DeviceManager.*",
                 "Input", "Input.*",
                 "Analise", "Analise.*",
                 "Emulate", "Emulate.*",
                 "Evaluate", "Evaluate.*",
                 "UI.DataGather"],
    ),

    keywords=[
        "EyeTrackFatigue",
    ],
    license="MIT",
)


'''
package_data={
    "EyeTrackFatigue_client": ["data/*.cfg"],
    },
    install_requires=[
        "requests==2.27.1",
    ],
    setup_requires=[
        "pytest-runner",
        "flake8==4.0.1",
    ],
    tests_require=[
        "pytest==7.1.2",
        "requests-mock==1.9.3",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
'''