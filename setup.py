# Copyright (c) 2022 Xingchen Song (sxc19@tsinghua.org.cn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys

from setuptools import find_packages, setup

# Determine package version robustly. Accept optional CLI arg `version=x.y.z` for CI flows,
# otherwise default to a package pre-release indicating Cantonese additions.
version = "1.0.4-yue"
try:
    # Look for an explicit 'version=...' argument and remove it from argv when present.
    for i, arg in enumerate(sys.argv[1:], start=1):
        if isinstance(arg, str) and arg.startswith("version="):
            version = arg.split("=", 1)[1]
            # remove the version arg so setuptools doesn't choke on it
            del sys.argv[i]
            break
except Exception:
    # If anything goes wrong, fall back to the default version above
    version = version

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name="WeTextProcessing",
    version=version,
    author="Zhendong Peng, Xingchen Song",
    author_email="pzd17@tsinghua.org.cn, sxc19@tsinghua.org.cn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="WeTextProcessing, including TN & ITN",
    url="https://github.com/wenet-e2e/WeTextProcessing",
    packages=find_packages(),
    package_data={
        "tn": [
            "*.fst",
            "chinese/data/*/*.tsv",
            "english/data/*/*.tsv",
            "english/data/*.tsv",
            "english/data/*/*.far",
            # Cantonese language data
            "cantonese/data/*/*.tsv",
            "cantonese/data/*.tsv",
        ],
        "itn": ["*.fst", "chinese/data/*/*.tsv"],
    },
    install_requires=["pynini==2.1.6", "importlib_resources"],
    # Optional extras for additional features; e.g., Cantonese simplified->traditional conversion
    extras_require={
        "cantonese": ["opencc-python-reimplemented"],
    },
    entry_points={
        "console_scripts": [
            "wetn = tn.main:main",
            "weitn = itn.main:main",
        ]
    },
    tests_require=["pytest", "opencc-python-reimplemented"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
