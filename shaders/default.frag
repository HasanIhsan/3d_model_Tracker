#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
flat in int material_id;  // Material ID passed from vertex shader

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0;  // Texture unit 0
uniform sampler2D u_texture_1;  // Texture unit 1
uniform sampler2D u_texture_2;  // Texture unit 2
uniform sampler2D u_texture_3;  // Texture unit 2
uniform sampler2D u_texture_4;  // Texture unit 2
uniform sampler2D u_texture_5;  // Texture unit 2
uniform sampler2D u_texture_6;  // Texture unit 2
uniform sampler2D u_texture_7;  // Texture unit 2
uniform sampler2D u_texture_8;  // Texture unit 2
uniform sampler2D u_texture_9;  // Texture unit 2
uniform sampler2D u_texture_10;  // Texture unit 2
uniform sampler2D u_texture_11;  // Texture unit 2
uniform sampler2D u_texture_12;  // Texture unit 2
uniform sampler2D u_texture_13; // Texture unit 13
uniform vec3 camPos;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);

    // Ambient light
    vec3 ambient = light.Ia;

    // Diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // Specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
};

void main() { 
    float gamma = 2.2;
    vec3 color;

    // Select texture based on material_id
    if (material_id == 0) {
        color = texture(u_texture_0, uv_0).rgb;
    } else if (material_id == 1) {
        color = texture(u_texture_1, uv_0).rgb;
    } else if (material_id == 2) {
        color = texture(u_texture_2, uv_0).rgb;
    }  else if (material_id == 3) {
        color = texture(u_texture_3, uv_0).rgb;
    }  else if (material_id == 4) {
        color = texture(u_texture_4, uv_0).rgb;
    }  else if (material_id == 5) {
        color = texture(u_texture_5, uv_0).rgb;
    }  else if (material_id == 6) {
        color = texture(u_texture_6, uv_0).rgb;
    }  else if (material_id == 7) {
        color = texture(u_texture_7, uv_0).rgb;
    }  else if (material_id == 8) {
        color = texture(u_texture_8, uv_0).rgb;
    }  else if (material_id == 9) {
        color = texture(u_texture_9, uv_0).rgb;
    }  else if (material_id == 10) {
        color = texture(u_texture_10, uv_0).rgb;
    }  else if (material_id == 11) {
        color = texture(u_texture_11, uv_0).rgb;
    }  else if (material_id == 12) {
        color = texture(u_texture_12, uv_0).rgb;
    }  else if (material_id == 13) {
        color = texture(u_texture_13, uv_0).rgb;
    }  












    color = pow(color, vec3(gamma));
    color = getLight(color);
    color = pow(color, 1 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}