import bpy
import numpy

def is_edit_change():
    
    current_object = bpy.context.active_object

    if current_object.type != 'MESH':
        return False
    
    temp_matrix_hash = str(hash(tuple(round(v,6) for row in current_object.matrix_world for v in row)))
        
    temp_modifier_count_hash = str(hash(len(current_object.modifiers)))
    
    temp_modifier_name_hash = str(hash(tuple(item.name for item in current_object.modifiers)))

        
    temp_vef_count_hash = str(hash((
                    len(current_object.data.vertices),
                    len(current_object.data.edges),
                    len(current_object.data.polygons),
                    )))

    temp_matrix_modifier_vefcount_hash = str(hash(
        temp_matrix_hash + temp_modifier_count_hash + temp_modifier_name_hash +temp_vef_count_hash
    ))

    if current_object.ba_data.matrix_modifier_vefcount_hash != temp_matrix_modifier_vefcount_hash:
        current_object.ba_data.matrix_modifier_vefcount_hash = temp_matrix_modifier_vefcount_hash
        return True
    
    temp_vertex_count = len(current_object.data.vertices)

    if temp_vertex_count < 5000:
        temp_vertex_position_hash = str(hash(tuple(round(vc,3) for vertex in current_object.data.vertices for vc in vertex.co)))
        if current_object.ba_data.vertex_position_hash != temp_vertex_position_hash:
            current_object.ba_data.vertex_position_hash = temp_vertex_position_hash
            return True
        
    if temp_vertex_count >= 5000:
        vertex_flat = [0.0]*len(current_object.data.vertices)*3
        current_object.data.vertices.foreach_get("co",vertex_flat)
        co_np = numpy.array(vertex_flat, dtype=numpy.float32).reshape(temp_vertex_count, 3)
        rounded_co = numpy.round(co_np, 3)
        temp_vertex_hash = str(hash(tuple(rounded_co.flatten())))

        if current_object.ba_data.vertex_position_hash != temp_vertex_hash:
            current_object.ba_data.vertex_position_hash = temp_vertex_hash
            return True

    return False
            

