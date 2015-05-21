from setuptools import setup, find_packages

setup(
        name = "ScreenCapture",
        version = "0.1.0",
        author = "LameStation",
        author_email = "contact@lamestation.com",
        description = "Take screenshots of LameStation games!",
        license = "GPLv3",
        url = "https://github.com/lamestation/ScreenCapture",
        keywords = "screen capture lamestation tools",
        scripts=['lscapture',],
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Programming Language :: Python :: 2 :: Only",
            "Programming Language :: Python :: 2.7",
            "Topic :: Games/Entertainment",
            "Topic :: Multimedia :: Graphics :: Viewers",
            ]
        )
