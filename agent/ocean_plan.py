"""Domain planner: research dependencies differ from production prerequisites."""
from agent.text import fold,tokens
from agent.engine import string

FACETS=[
 ('collision','MeshPart collisions CanCollide','rendering',10,['CollisionFidelity','CanCollide','CollisionGroup'],['Roblox collision groups CanCollide','MeshPart collision fidelity performance']),
 ('cards','foliage cards transparency','spruce',9,['foliage','transparency','alpha'],['SurfaceAppearance AlphaMode transparency','foliage atlas normals']),
 ('geometry','spruce branch geometry','spruce',8,['mesh','branch','geometry'],['tree silhouette mesh topology']),
 ('materials','SurfaceAppearance PBR textures','rendering',8,['SurfaceAppearance','ColorMap','NormalMap'],['Roblox roughness normal textures']),
 ('snow','snow branch accumulation','snow',8,['snow','mesh','material'],['Roblox snow mesh materials']),
 ('ground','snow terrain footprints','terrain',7,['terrain','snow','footprint'],['Roblox terrain snow decals']),
 ('night','night forest Atmosphere fog','lighting',8,['Atmosphere','lighting','fog'],['Roblox night lighting contrast']),
 ('flashlight','SpotLight flashlight shadows','lighting',8,['SpotLight','Shadows','Range'],['Roblox flashlight shadow performance']),
 ('wind','tree wind bones animation','spruce',6,['bone','animation','wind'],['Roblox skinned mesh foliage']),
 ('performance','forest placement streaming LOD','performance',9,['streaming','LOD','performance'],['Roblox dense forest MicroProfiler']),
 ('export','Blender mesh FBX export Roblox','rendering',7,['mesh','export','transform'],['Blender FBX normals scale']),
 ('comparison','Unreal foliage Roblox limitations','rendering',5,['foliage','Unreal','Roblox'],['Roblox vegetation rendering limitations'])]


def describe(goal):
    string(goal,'goal')
    import re
    words=set(tokens(goal));forest=bool(re.search(r'\b(?:foret|forest|sapins?|spruce|epiceas?|arbres?|trees?)\b',fold(goal)))
    if not forest:
        selected=[f for f in FACETS if set(tokens(f[1]))&words]
    else:selected=FACETS
    nodes=[{'id':f[0],'query':f[1],'topic':f[2],'priority':f[3],'requires':[],
            'production_prerequisites':['asset copies','version and device','repeatable camera and controls'],
            'anchors':f[4],'followups':f[5],
            'reason':'document independent technical gap; prerequisite for production is not a research blockade'} for f in selected]
    return {'schema':'vdn.ocean-plan/11','goal':goal,'profile':'snowy_forest' if forest else 'bounded_domain_fallback' if nodes else 'unmapped_goal',
            'nodes':nodes,'method':'curated domain decomposition and gap priorities; no model reasoning claimed',
            'truth_verified':False,'network_requests':0}


def facet_for(query):
    words=set(tokens(query))
    return max(FACETS,key=lambda f:len(words&set(tokens(f[1]))))
