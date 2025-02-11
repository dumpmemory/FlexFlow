# Copyright 2023 CMU, Facebook, LANL, MIT, NVIDIA, and Stanford (alphabetical)
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

import os, platform
from typing import Any, Union

from .flexflow_cffi_header import flexflow_header

from legion_cffi import ffi

class FlexFlowLib(object):
    __slots__ = ['_lib', '_header']
    def __init__(self) -> None:
        self._lib: Union[Any, None] = None
        self._header = flexflow_header

    @property
    def lib(self) -> Any:
        assert self._lib is not None
        return self._lib

    def get_name(self) -> str:
        return "flexflow"

    def get_library_extension(self) -> str:
        os_name = platform.system()
        if os_name == "Linux":
            return ".so"
        elif os_name == "Darwin":
            return ".dylib"
        else:
            assert 0, "unknown platform"

    def get_shared_library(self) -> str:
        libname = "libflexflow" + self.get_library_extension()
        return os.path.join(libname)

    def get_c_header(self) -> str:
        return self._header

    def initialize(self) -> None:
        shared_lib_path = self.get_shared_library()
        ffi.cdef(self._header)
        self._lib = ffi.dlopen(shared_lib_path)
        self._lib.flexflow_perform_registration()

    def destroy(self) -> None:
        print("destroy corelib")


flexflow_library = FlexFlowLib()