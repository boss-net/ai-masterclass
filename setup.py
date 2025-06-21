from setuptools import setup, find_packages

setup(
    name="bosskit",
    version="0.1.0",
    description="BossNet AI Agent Toolkit",
    packages=[
        'modules',
        'modules.agent_basics',
        'modules.agent_basics.tests',
        'modules.langchain_intro',
        'modules.langchain_intro.tests',
        'modules.retrieval_augmented_generation',
        'modules.retrieval_augmented_generation.tests',
        'modules.task_orchestration',
        'modules.task_orchestration.tests'
    ],
    package_dir={
        '': '.'
    },
    install_requires=[
        'streamlit>=1.28.0',
        'asana>=0.11.0',
        'langchain>=0.1.0',
        'pytest>=7.4.0',
        'pytest-cov>=4.1.0',
        'black>=22.12.0',
        'flake8>=6.1.0',
        'safety>=2.3.4'
    ],
    python_requires=">=3.13",
)
