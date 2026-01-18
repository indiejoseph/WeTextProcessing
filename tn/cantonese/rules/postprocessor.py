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

from pynini import difference, string_file, accep, cross
from pynini.lib.pynutil import delete, insert
from pynini.lib.tagger import Tagger

from tn.processor import Processor
from tn.utils import get_abs_path


class PostProcessor(Processor):

    def __init__(
        self,
        remove_interjections=True,
        remove_puncts=False,
        full_to_half=True,
        tag_oov=False,
    ):
        super().__init__(name="postprocessor")
        blacklist = string_file(get_abs_path("cantonese/data/default/blacklist.tsv"))
        puncts = string_file(get_abs_path("cantonese/data/char/punctuations_zh.tsv"))
        full2half = string_file(
            get_abs_path("cantonese/data/char/fullwidth_to_halfwidth.tsv")
        )
        zh_charset_std = string_file(
            get_abs_path("cantonese/data/char/charset_national_standard_2013_8105.tsv")
        )
        zh_charset_ext = string_file(
            get_abs_path("cantonese/data/char/charset_extension.tsv")
        )

        processor = self.build_rule("")
        # Apply Cantonese-specific overrides (simplified->Cantonese Traditional)
        try:
            cantonese_overrides = string_file(
                get_abs_path("cantonese/data/char/cantonese_overrides.tsv")
            )
        except Exception:
            cantonese_overrides = None
        if cantonese_overrides is not None:
            processor @= self.build_rule(cantonese_overrides)

        if remove_interjections:
            processor @= self.build_rule(delete(blacklist))

        if remove_puncts:
            processor @= self.build_rule(delete(puncts | self.PUNCT))

        if full_to_half:
            processor @= self.build_rule(full2half)

        # Cantonese-specific currency handling: treat HKD / HK$ / $ as Cantonese dollars ('蚊')
        hk_currency = accep("HKD") | accep("HK＄") | accep("HK$") | accep("$")
        # insert '蚊' for HK currency tokens so value+蚊 forms appear after verbalizer
        processor @= self.build_rule(
            insert("蚊") + delete('currency: "') + hk_currency + delete('"')
        )
        # Also replace verbalized currency names like '美元' or '港元' with '蚊'
        processor @= self.build_rule(
            cross("美元", "蚊") | cross("港元", "蚊") | cross("港幣", "蚊")
        )
        # decimal handling: 點五蚊 -> 個半 ; 點X蚊 -> 個X (drop 蚊 for decimal case)
        processor @= self.build_rule(cross("點五蚊", "個半"))
        for d in ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]:
            processor @= self.build_rule(cross("點" + d + "蚊", "個" + d))

        if tag_oov:
            charset = (
                zh_charset_std
                | zh_charset_ext
                | puncts
                | self.DIGIT
                | self.ALPHA
                | self.PUNCT
                | self.SPACE
            )
            oov = difference(self.VCHAR, charset)
            processor @= Tagger("oov", oov, self.VSIGMA)._tagger

        self.processor = processor.optimize()
