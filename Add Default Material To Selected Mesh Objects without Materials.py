bl_info = {
    "name": "Add Default Material To Selected Mesh Objects without Materials",
    "author": "DeepSeek, Le Chat, Gemini, Rimuru1201",
    "version": (1, 3),
    "blender": (4, 4, 3),
    "location": "视图 >> 物体模式 >> 选择",
    "description": "为没有材质的物体添加默认材质",
    "category": "Mesh",
}

import bpy
from bpy.types import Operator, Panel
from bpy.props import BoolProperty

# 获取或创建默认材质
def get_default_material():
    mat = bpy.data.materials.get("DefaultMaterial")
    
    if mat is None:
        # 创建新材质
        mat = bpy.data.materials.new(name="DefaultMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        principled = nodes[0]
        
        if principled:
            # 设置材质属性
            principled.inputs['Base Color'].default_value = (0.631, 0.631, 0.631, 1.0)  # #A1A1A1
            principled.inputs['Metallic'].default_value = 1.0
            principled.inputs['Roughness'].default_value = 0.0
            # 设置材质为金属工作流
            mat.metallic = 1.0
            mat.roughness = 0.0
    
    return mat

# 为选中物体添加材质
class OBJECT_OT_add_default_metallic_to_selected(Operator):
    bl_idname = "object.add_default_metallic_selected"
    bl_label = "Add DefaultMaterial to Selected"
    bl_description = "Add DefaultMaterial to selected mesh objects without materials"
    
    def execute(self, context):
        get_default_material()
        
        # 获取选中的网格物体
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected!")
            return {'CANCELLED'}
        
        # 处理物体
        count = 0
        mat = bpy.data.materials.get("DefaultMaterial")
        for obj in selected_meshes:
            if not obj.data.materials:
                obj.data.materials.append(mat)
                count += 1
        
        self.report({'INFO'}, f"Added material to {count} selected objects")
        return {'FINISHED'}

# 添加菜单项
def menu_func(self, context):
    self.layout.operator(OBJECT_OT_add_default_metallic_to_selected.bl_idname, icon='MATERIAL_DATA')

# 注册
def register():
    # 注册类和处理器
    bpy.utils.register_class(OBJECT_OT_add_default_metallic_to_selected)
    bpy.types.VIEW3D_MT_add.append(menu_func)
    
# 注销
def unregister():
    # 注销类和菜单项
    bpy.utils.unregister_class(OBJECT_OT_add_default_metallic_to_selected)
    bpy.types.VIEW3D_MT_add.remove(menu_func)

# 直接运行时注册
if __name__ == "__main__":
    register()