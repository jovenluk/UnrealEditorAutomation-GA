

#include "CppLib.h"

// PublicDependencyModuleNames -> "PythonScriptPlugin" && "Python"
#include "../Plugins/Experimental/PythonScriptPlugin/Source/PythonScriptPlugin/Private/PythonScriptPlugin.h"

void UCppLib::ExecutePythonScript(FString PythonScript) {
	FPythonScriptPlugin::Get()->ExecPythonCommand(*PythonScript);
}

// Load Static Mesh From Path 
 UStaticMesh* UCppLib::LoadMeshFromPath(const FName& Path)
{
	if (Path == NAME_None) return NULL;
	//~

	return LoadObjFromPath<UStaticMesh>(Path);
}

