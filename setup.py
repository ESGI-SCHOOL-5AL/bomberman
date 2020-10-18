from setuptools import setup

setup(
    name="bomberman",
    version="0.5.0",
    description="Bomberman game with reinforcement learning for ESGI project",
    author="akurtaliqi, System-Glitch, ulphidius",
    install_requires=[
        "arcade"
    ],
    entry_points={
        "console_script": [
            "bomberman = main"
        ]
    }
)
