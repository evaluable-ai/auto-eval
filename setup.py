from setuptools import setup, find_packages

setup(
    name='evaluableai',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'annotated-types==0.6.0',
        'anyio==3.7.1',
        'certifi==2023.7.22',
        'charset-normalizer==3.3.2',
        'distro==1.8.0',
        # 'evaluableai @ file:///Users/pgargr/PycharmProjects/clean/LLM-eval', # Local path, not included
        'h11==0.14.0',
        'httpcore==1.0.2',
        'httpx==0.25.1',
        'idna==3.4',
        'numpy==1.26.2',
        'openai==1.3.2',
        'pandas==2.1.3',
        'pydantic==2.5.1',
        'pydantic_core==2.14.3',
        'python-dateutil==2.8.2',
        'pytz==2023.3.post1',
        'requests==2.31.0',
        'six==1.16.0',
        'sniffio==1.3.0',
        'tqdm==4.66.1',
        'typing_extensions==4.8.0',
        'tzdata==2023.3',
        'urllib3==2.1.0'
    ],
    # Other metadata
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
