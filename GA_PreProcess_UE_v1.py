# -*- coding: utf-8 -*-

import unreal as ue
import sys


def log_unreal(cad):
    """
    logs hello unreal to the output log in unreal
    """
    ue.log_warning(cad)


# SIGNATURE
log_unreal("GA_PreProcess_UE_v1.py --> Version 1.0")


# =============================================================================
# --- Funciones importantes
# =============================================================================
# leer una instancia
    # chair_asset = ue.load_asset('/Game/StarterContent/Props/SM_Chair.SM_Chair')
# leer una propiedad de un objeto (para ponerle un valor se usa set_editor_property)
    # chair_asset = ue.get_editor_property("")
# como trabajar con los helpers de unreal
    # utility_base = ue.GlobalEditorUtilityBase.get_default_object()
    # selected_assets = utility_base.get_selected_assets()

# =============================================================================
# --- Put the sockets with parameters to decide localization
# =============================================================================
def GA_putSockets(static_meshes, sockets_orientation = "y", reverse = False, alignment = "center", top_and_down = False):
    # SIGNATURE
    log_unreal("GA_putSockets static_meshes = {static_meshes}".format(
        static_meshes = static_meshes))
    # static_meshes = static_meshes if isinstance(static_meshes, list) else [static_meshes]

    for static_mesh in static_meshes:

        # get the origin of the mesh bounds
        extent = static_mesh.get_bounding_box()

        # si existen previamente sockets llamados L y R, nos los cargamos
        sockets = ["L", "R"]
        for i in sockets:
            result = static_mesh.find_socket(i)
            if result != None:
                static_mesh.remove_socket(result)

        # creación vacía de los sockets. IMPORTANTE asignarlos SIEMPRE a un "outer" !!!!!!
        socketL = ue.StaticMeshSocket(static_mesh) # OJO con el constructor. El outer SIEMPRE tiene que tener el ojbeto al que pertenece. UNREAL hace un crash si esto está vacío porque no sabe resolverlo.
        socketL.set_editor_property("socket_name", "L")
        cadena = "GA_putSockets: Created socket name {name_socket} in StaticMesh name {name_static_mesh}".format(
            name_socket = "L",
            name_static_mesh = static_mesh.get_name()
            )
        log_unreal(cadena)

        socketR = ue.StaticMeshSocket(static_mesh)
        socketR.set_editor_property("socket_name", "R")
        cadena = "GA_putSockets: Created socket name {name_socket} in StaticMesh name {name_static_mesh}".format(
            name_socket = "R",
            name_static_mesh = static_mesh.get_name()
            )
        log_unreal(cadena)

        # values to create vectors for sockets L and R
        xL = 0
        xR = 0
        yL = 0
        yR = 0
        zL = 0
        zR = 0
        # values to create vectors for sockets T and B
        xT = 0
        xB = 0
        yT = 0
        yB = 0
        zT = 0
        zB = 0

        if sockets_orientation == "x":

            xL = extent.max.x
            xR = extent.min.x
            yL = 0
            yR = 0
            zL = 0
            zR = 0

            if alignment == "center":

                yL = 0
                yR = 0


            if alignment == "external":

                yL = extent.max.y
                yR = extent.max.y


            if alignment == "internal":

                yL = extent.min.y
                yR = extent.min.y

        if sockets_orientation == "y":

            xL = 0
            xR = 0
            yL = extent.max.y
            yR = extent.min.y
            zL = 0
            zR = 0

            if alignment == "center":

                xL = 0
                xR = 0


            if alignment == "external":

                xL = extent.max.x
                xR = extent.max.x



            if alignment == "internal":

                xL = extent.min.x
                xR = extent.min.x

        if sockets_orientation == "z": # es el equivalente a los sockets TOP y BOTTOM

            xL = 0
            xR = 0
            yL = 0
            yR = 0
            zL = extent.max.z
            zR = extent.min.z

            if alignment == "center":

                xL = 0
                xR = 0


            if alignment == "external":

                xL = extent.max.x
                xR = extent.max.x



            if alignment == "internal":

                xL = extent.min.x
                xR = extent.min.x




        # creamos los sockets
        if reverse == False:
            socketL.set_editor_property("relative_location", ue.Vector(xL,yL,zL))
            socketR.set_editor_property("relative_location", ue.Vector(xR,yR,zR))
        else:
            socketL.set_editor_property("relative_location", ue.Vector(xR,yR,zR))
            socketR.set_editor_property("relative_location", ue.Vector(xL,yL,zL))

        # añadimos los sockets
        static_mesh.add_socket(socketL)
        static_mesh.add_socket(socketR)

    # SIGNATURE
    log_unreal("GA_putSockets return static_meshes = {static_meshes}".format(
        static_meshes = static_meshes))

    return static_meshes



# =============================================================================
# # PARAMETROS QUE RECIBE EL SCRIPT
# =============================================================================
sockets_orientation = "x"
reverse = False
alignment = "center"
top_and_down = "false"
destination_path = "GA_BP_ASSETS"
suffix = "_WithSockets"

# =============================================================================
# ---- Actualizar Assets
# =============================================================================
def GA_saveAssets(static_meshes):
    # SIGNATURE
    log_unreal("GA_saveAssets static_meshes = {static_meshes}".format(
        static_meshes = static_meshes))
    # static_meshes = static_meshes if isinstance(static_meshes, list) else [static_meshes]

    for static_mesh in static_meshes:
        path = static_mesh.get_full_name()
        ue.EditorAssetLibrary.save_asset( path, False)
        # ue.EditorAssetLibrary.checkout_asset(path)

# =============================================================================
# ---- Duplica assets en un directorio y con un sufijo concreto
# =============================================================================
def GA_duplicateAssets(static_meshes, destination_path = destination_path, suffix = suffix):
    # SIGNATURE
    log_unreal("GA_duplicateAssets static_meshes = {static_meshes}, destination_path = {destination_path}, suffix = {suffix}".format(
        static_meshes = static_meshes,
        destination_path = destination_path,
        suffix = suffix))
    new_assets = []
    asset_tools = ue.EditorAssetLibrary.get_default_object()
    for static_mesh in static_meshes:

        source_asset_path = static_mesh.get_full_name()
        new_asset_name = '{name}{suffix}'.format(
            name = static_mesh.get_name(),
            suffix = suffix)
        destination_asset_path = '/Game/{destination_path}/{new_asset_name}'.format(
            destination_path = destination_path,
            new_asset_name = new_asset_name)
        new_static_mesh = asset_tools.duplicate_asset(source_asset_path, destination_asset_path)
        new_assets.append(new_static_mesh)
    # SIGNATURE
    log_unreal("GA_duplicateAssets return new_assets = {new_assets}".format(
        new_assets = new_assets))
    return new_assets


# =============================================================================
# ---- PRUEBA para hacer CAST
# =============================================================================

def cast(object_to_cast, object_class):
    try:
        return object_class.cast(object_to_cast)
    except:
        return None

# ejemplo de uso
        # cast(selected_asset, ue.Actor)



# =============================================================================
# FIN PRUEBA CAST
# =============================================================================

def updatePropertyInBlueprint(blueprint_name, field_name, value):
    # selecciono los BP con los que quiero jugar
    # utility_base = ue.GlobalEditorUtilityBase.get_default_object()
    # selected_assets = utility_base.get_selected_assets()

    # selected_assets = list(selected_assets)
    # le añado "_C" al blueprint que quiero cargar para poder trabajar con sus propiedades
    # reference = '/Game/Meshes/BP/BP_ChairWithSignals.BP_ChairWithSignals_C'

    log_unreal("updatePropertyInBlueprint blueprint_name = {blueprint_name}, field_name = {field_name}, value = {value}".format(
        blueprint_name = blueprint_name,
        field_name = field_name,
        value = value))

    reference = blueprint_name


    # get the generated class of the Blueprint (note the _C)
    bp_gc = ue.load_object(None, reference)
    # get the Class Default Object (CDO) of the generated class
    bp_cdo = ue.get_default_object(bp_gc)
    # set the default property values
    # OJO que la propiedad tiene que estar creada previamente!!!!
    bp_cdo.set_editor_property(field_name, value)
    # bp_cdo.set_editor_property("MyBoolProp", True)
    # como conseguir acceso a los componentes, funciones, etc...?




# =============================================================================
# ---- PROGRAM
# =============================================================================

# selected_assets = ue.EditorUtilityLibrary.get_selected_assets()
utility_base = ue.GlobalEditorUtilityBase.get_default_object()
selected_assets = utility_base.get_selected_assets()

selected_assets = list(selected_assets)

# get arguments
script_to_execute = sys.argv[1]
# sockets_orientation = sys.argv[2]
# reverse = sys.argv[3]
# alignment = sys.argv[4]
# top_and_down = sys.argv[5] # está previsto para poner sockets arriba y abajo en los elementos, pero todavía no lo tengo implementado
# destination_path = sys.argv[6]
# suffix = sys.argv[7]


if script_to_execute == "GA_Preprocess_Sockets":
    sockets_orientation = sys.argv[2]
    reverse = sys.argv[3]
    alignment = sys.argv[4]
    top_and_down = sys.argv[5] # está previsto para poner sockets arriba y abajo en los elementos, pero todavía no lo tengo implementado
    destination_path = sys.argv[6]
    suffix = sys.argv[7]

if script_to_execute == "GA_Preprocess_Change_Value":
    blueprint_name = sys.argv[2]
    field_name = sys.argv[3]
    value = sys.argv[4]

if reverse == "true":
    reverse = True
else:
    reverse = False

if top_and_down == "true":
    top_and_down = True
else:
    top_and_down = False

# selected_assets = GA_putSockets(selected_assets, sockets_orientation = sockets_orientation, reverse = reverse, alignment = alignment, top_and_down = top_and_down)
# GA_saveAssets(selected_assets) # grabamos los cambios


if script_to_execute == "GA_Preprocess_Sockets":
    selected_assets = GA_duplicateAssets(selected_assets, destination_path = destination_path, suffix = suffix) # duplicamos los assets
    selected_assets = list(selected_assets)
    selected_assets = GA_putSockets(selected_assets, sockets_orientation = sockets_orientation, reverse = reverse, alignment = alignment, top_and_down = top_and_down)
    GA_saveAssets(selected_assets) # grabamos los cambios

if script_to_execute == "GA_Preprocess_Change_Value":
    updatePropertyInBlueprint(blueprint_name, field_name, value)


# estamos seleccionando en el Content Browser, pero podrían cogerse todos los assets que estén en una carpeta directamente
# aprovechando para calificar el estilo de cada asset (que se utiliza por el GA) en función del nombre de la carpeta


# =============================================================================
# ---- END PROGAM
# =============================================================================

# https://github.com/mamoniem/UnrealEditorPythonScripts/blob/master/Assets/OrganizeAssetsPerType.py
# https://forums.unrealengine.com/development-discussion/content-creation/1698621-replacing-static-mesh-actor-with-blueprint-class

def Pruebas():
    print(editorAssetLib.find_asset_data(bp[0].get_path_name()))


# =============================================================================
# Todos los actores al punto 0,0,0
# =============================================================================
def todosLosActoresAlPuntoZero():
    import unreal
    from unreal import Vector

    lst_actors = unreal.EditorLevelLibrary.get_all_level_actors()

    print('place actors at 0 z')
    for act in lst_actors:
        act_label = act.get_actor_label()
        if 'Sphere_' in act_label:
            print('placing: {}'.format(act_label))
            act_location = act.get_actor_location()
            act_bounds = act.get_actor_bounds(False)
            act_min_z = act_bounds[0].z - act_bounds[1].z
            location_offset = Vector(act_location.x, act_location.y, act_location.z - act_min_z)
            act.set_actor_location(location_offset, False, False)

# =============================================================================
# ---- SLOW OPERATIONS DIALOG
# source: https://docs.unrealengine.com/en-US/Engine/Editor/ScriptingAndAutomation/Python/index.html
# =============================================================================
def slowOperationsDialog():
    import unreal
    total_frames = 100
    text_label = "Working!"
    with unreal.ScopedSlowTask(total_frames, text_label) as slow_task:
        slow_task.make_dialog(True)               # Makes the dialog visible, if it isn't already
        for i in range(total_frames):
            if slow_task.should_cancel():         # True if the user has pressed Cancel in the UI
                break
            slow_task.enter_progress_frame(1)     # Advance progress by one frame.
                                                # You can also update the dialog text in this call, if you want.
    #         ...                                   # Now do work for the current frame here!

# =============================================================================
# FIN SLOW OPERATIONS
# =============================================================================

# =============================================================================
# ---- Prueba para crear un Blueprint
# =============================================================================
def pruebaParaCrearUnBlueprint():
    import unreal

    asset_name = "BP_New1"
    package_path = "/Game/MyContentFolder"

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("ParentClass", unreal.Actor)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp = asset_tools.create_asset(asset_name, package_path, None, factory)

    unreal.EditorAssetLibrary.save_loaded_asset(bp)

# =============================================================================
# Fin Prueba para crear un Blueprint
# =============================================================================


# =============================================================================
#  Adding Simplified Collissions
#  source: https://docs.unrealengine.com/en-US/Engine/Editor/ScriptingAndAutomation/HowTos/SettingUpCollisionProperties/index.html
# =============================================================================
def simplifiedCollissions():
    import unreal
    asset_path = "/Game/ArchVis/Mesh"
    def add_box_collision (static_mesh):
        # You could instead use .SPHERE, .CAPSULE, .NDOP10_X, .NDOP10_Y, .NDOP10_Z, .NDOP18, .NDOP26
        shape_type = unreal.ScriptingCollisionShapeType.BOX
        unreal.EditorStaticMeshLibrary.add_simple_collisions(static_mesh, shape_type)
        unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)
    # get a list of all Assets in the path.
    all_assets = unreal.EditorAssetLibrary.list_assets(asset_path)
    # load them all into memory.
    all_assets_loaded = [unreal.EditorAssetLibrary.load_asset(a) for a in all_assets]
    # filter the list to include only Static Meshes.
    static_mesh_assets = unreal.EditorFilterLibrary.by_class(all_assets_loaded, unreal.StaticMesh)
    # run the function above on each Static Mesh in the list.
    map(add_box_collision, static_mesh_assets)

# =============================================================================
# Fin Add Simplified Collissions
# =============================================================================






# =============================================================================
# Deal with properties in blueprint
# FUNCIONA!!!!!
# =============================================================================
def dealWithPropertiesInBlueprint():
    # selecciono los BP con los que quiero jugar
    # utility_base = ue.GlobalEditorUtilityBase.get_default_object()
    # selected_assets = utility_base.get_selected_assets()

    # selected_assets = list(selected_assets)
    # le añado "_C" al blueprint que quiero cargar para poder trabajar con sus propiedades
    reference = '/Game/Meshes/BP/BP_ChairWithSignals.BP_ChairWithSignals_C'
    # get the generated class of the Blueprint (note the _C)
    bp_gc = unreal.load_object(None, reference)
    # get the Class Default Object (CDO) of the generated class
    bp_cdo = unreal.get_default_object(bp_gc)
    # set the default property values
    # OJO que la propiedad tiene que estar creada previamente!!!!
    bp_cdo.set_editor_property("MyFloatProp", 11.135)
    bp_cdo.set_editor_property("MyBoolProp", True)
    # como conseguir acceso a los componentes, funciones, etc...?






    # parece que esta función ayuda a coger nodos y a crear nodos en un blueprint
    # BTFunctionLibrary

    # como conseguir el ParentClass de un blueprint
    bpFactory = ue.BlueprintFactory().get_default_object()

    ue.Class(name=bp_cdo.get_name()) # nos devuelve la clase de un objeto... a ver si funciona (es equivalente a type(Class) que aparece en la documentación)

    # como instanciar un StaticMesh
    unreal.EditorLevelLibrary().spawn_actor_from_class(ue.StaticMeshActor.static_class(), location, rot)



