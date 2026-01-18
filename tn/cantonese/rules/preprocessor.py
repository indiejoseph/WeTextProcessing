# Copyright (c) 2022 Zhendong Peng (pzd17@tsinghua.org.cn)
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

from pynini import string_file

from tn.processor import Processor
from tn.utils import get_abs_path


class PreProcessor(Processor):

    def __init__(self, traditional_to_simple=True, simple_to_traditional=False):
        super().__init__(name="preprocessor")
        traditional2simple = string_file(
            get_abs_path("cantonese/data/char/traditional_to_simple.tsv")
        )
        simple2traditional = string_file(
            get_abs_path("cantonese/data/char/simple_to_traditional.tsv")
        )
        # optional Cantonese-specific overrides (e.g., 吃 -> 喫)
        try:
            cantonese_overrides = string_file(
                get_abs_path("cantonese/data/char/cantonese_overrides.tsv")
            )
        except Exception:
            cantonese_overrides = None

        processor = self.build_rule("")
        if traditional_to_simple:
            processor @= self.build_rule(traditional2simple)
        if simple_to_traditional:
            # We avoid broad simple->traditional conversion here for Cantonese normalizer
            processor @= self.build_rule(simple2traditional)
        if cantonese_overrides is not None:
            processor @= self.build_rule(cantonese_overrides)

        self.processor = processor.optimize()
