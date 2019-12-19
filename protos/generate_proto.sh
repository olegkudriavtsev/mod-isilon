#!/usr/bin/env bash
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    PROTOC_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "linux_x64" | sort -r | head -1)/protoc"
    CSHARP_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "linux_x64" | sort -r | head -1)/grpc_csharp_plugin"
elif [[ "$OSTYPE" == "win32" || "$OSTYPE" == "msys" ]];  then
    PROTOC_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "windows_x86")/protoc.exe"
    CSHARP_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "windows_x86")/grpc_csharp_plugin.exe"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    PROTOC_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "macosx_x64" | sort -r | head -1)/protoc"
    CSHARP_PLUGIN_LOCATION="$(find ~/.nuget/packages/grpc.tools -name "macosx_x64" | sort -r | head -1)/grpc_csharp_plugin"
fi

if [[ -z "$PROTOC_PLUGIN_LOCATION" ]]; then
    echo "Can't find gRPC as a Nuget package. Please install it. Aborting."; exit 1;
fi

CSHARP_RESULT_PATH=${ROOT_DIR}/../src/Faction.Isilon.Grpc/v1/Services
for FILE in $(find ${ROOT_DIR} -type f -name "*.proto")
do 
   "${PROTOC_PLUGIN_LOCATION}" -I "${ROOT_DIR}" -I. --csharp_out ${CSHARP_RESULT_PATH} --grpc_out ${CSHARP_RESULT_PATH} ${FILE} --plugin=protoc-gen-grpc="${CSHARP_PLUGIN_LOCATION}"
   python -m grpc_tools.protoc -I "${ROOT_DIR}" -I. --python_out=../server --grpc_python_out=../server ${FILE}
done
