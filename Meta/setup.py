from setuptools import find_packages, setup


def get_long_description():
    return 'https://github.com/AI-group-72/FAEyeTON/blob/main/README.md'

def get_requirements():
    return ['pandas', 'openpyxl', 'scikit-learn', 'numpy', 'PyQt6', 'opencv-python', 'joblib']

setup(
    name="EyeTrackFatigue",
    version="1.0.14",
    description="проект FAEyeTON - Библиотека открытого кода для оценки функционального состояния утомления оператора на основе динамической активности взгляда и головы. Проект Код-ИИ-2022.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Кашевник А.М. Кузнецов В.В. Брак И.В. Мамонов А.А. Коваленко С.Д.",
    author_email="anton.mamonov.golohvastogo@mail.ru",
    url="https://github.com/AI-group-72/FAEyeTON",
    project_urls={
        "GitHub Project": "https://github.com/AI-group-72/FAEyeTON",
        "Issue Tracker": "https://github.com/AI-group-72/FAEyeTON/Meta/issues",
    },
    packages=['EyeTrackFatigue.DeviceManager', 'EyeTrackFatigue.Input',
              'EyeTrackFatigue.Analise', 'EyeTrackFatigue.Evaluate', 'EyeTrackFatigue.UI', 'EyeTrackFatigue.Meta'],
    install_requires=get_requirements(),
    python_requires=">=3.12",

    keywords=[
        "EyeTrackFatigue",
    ],
    license="GNU LGPL",
)



