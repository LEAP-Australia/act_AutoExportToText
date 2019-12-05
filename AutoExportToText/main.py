'''
Copyright 2019 LEAP Australia Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Nish Joseph
'''

from os.path import abspath
from os.path import join as joinpath

# pylint: disable=missing-docstring
class SelectResultObj:
    # pylint: disable=no-self-use
    # pylint: disable=unused-argument

    def __init__(self, api, entity, prop):
        self.api = api

    def get_result_objs(self, obj):
        # pylint: disable=broad-except
        # pylint: disable=unused-variable
        # pylint: disable=bare-except
        results = []
        for child in obj.Analysis.Solution.Children:
            try:
                test = child.ExportToTextFile
                results.append(child)
            except:
                pass
        return results

    def getvalue(self, obj, prop, val):
        if val is None:
            return None
        results = self.get_result_objs(obj)
        for res in results:
            if res.ObjectId == int(val):
                return res
        return None

    def onactivate(self, obj, prop):
        prop.Options.Clear()
        results = self.get_result_objs(obj)
        for res in results:
            prop.Options.Add(str(res.ObjectId))

    def value2string(self, obj, prop, val):
        result = None
        if val is not None:
            results = self.get_result_objs(obj)
            for res in results:
                if res.ObjectId == int(val):
                    result = res
                    break
        if result is None:
            return ''
        return result.Name

    def isvalid(self, obj, prop):
        return prop.Value is not None

def exportToText(obj, func):
    try:
        result = obj.Properties['ResObj'].Value
        out_path = ExtAPI.Application.InvokeUIThread(
            lambda: abspath(joinpath(obj.Analysis.WorkingDir, '../../../user_files')))  
        file_path = joinpath(out_path, obj.Properties['filePath'].Value)
        ExtAPI.Log.WriteError(file_path)
        ExtAPI.Application.InvokeUIThread(
            lambda: result.ExportToTextFile(file_path))
        return True
    except:
        pass
    return False
