#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
layout (location = 3) in int in_material_id;  // Material ID attribute

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;
flat out int material_id;  // Pass material ID to fragment shader

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;
//uniform int material_id;


void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    material_id = in_material_id;  // Pass material ID
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}