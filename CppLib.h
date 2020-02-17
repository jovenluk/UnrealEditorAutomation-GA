// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "CppLib.generated.h"

UCLASS()
class ESCAPEFROMTHECASTLE_API UCppLib : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()
public:
	UFUNCTION(BlueprintCallable, Category = "FGV Functions")
		static void ExecutePythonScript(FString PythonScript);

	UFUNCTION(BlueprintCallable, Category = "FGV Functions")
		static UStaticMesh* LoadMeshFromPath(const FName& Path);


};


//TEMPLATE Load Obj From Path
template <typename ObjClass>
static FORCEINLINE ObjClass* LoadObjFromPath(const FName& Path)
{
	if (Path == NAME_None) return NULL;
	//~

	return Cast<ObjClass>(StaticLoadObject(ObjClass::StaticClass(), NULL, *Path.ToString()));
}
