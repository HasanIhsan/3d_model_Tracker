#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos; 

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
uniform sampler2D u_texture_14; // Texture unit 13
uniform sampler2D u_texture_15; // Texture unit 13
uniform sampler2D u_texture_16; // Texture unit 13
uniform sampler2D u_texture_17; // Texture unit 13
uniform sampler2D u_texture_18; // Texture unit 13
uniform sampler2D u_texture_19; // Texture unit 13
uniform sampler2D u_texture_20; // Texture unit 13
uniform sampler2D u_texture_21; // Texture unit 13
uniform sampler2D u_texture_22; // Texture unit 13
uniform int material_id;

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
    vec3 color = vec3(0.0);  // Default to black

    if (material_id == 0) {
        color = texture(u_texture_0, uv_0).rgb;
    } else if (material_id == 1) {
        color = mix(color, texture(u_texture_1, uv_0).rgb, 0.5);
    } else if (material_id == 2) {
        color = mix(color, texture(u_texture_2, uv_0).rgb, 0.5);
    } else if (material_id == 3) {
        color = mix(color, texture(u_texture_3, uv_0).rgb, 0.5);
    } else if (material_id == 4) {
        color = mix(color, texture(u_texture_4, uv_0).rgb, 0.5);
    } else if (material_id == 5) {
        color = mix(color, texture(u_texture_5, uv_0).rgb, 0.5);
    } else if (material_id == 6) {
        color = mix(color, texture(u_texture_6, uv_0).rgb, 0.5);
    } else if (material_id == 7) {
        color = mix(color, texture(u_texture_7, uv_0).rgb, 0.5);
    } else if (material_id == 8) {
        color = mix(color, texture(u_texture_8, uv_0).rgb, 0.5);
    } else if (material_id == 9) {
        color = mix(color, texture(u_texture_9, uv_0).rgb, 0.5);
    } else if (material_id == 10) {
        color = mix(color, texture(u_texture_10, uv_0).rgb, 0.5);
    } else if (material_id == 11) {
        color = mix(color, texture(u_texture_11, uv_0).rgb, 0.5);
    } else if (material_id == 12) {
        color = mix(color, texture(u_texture_12, uv_0).rgb, 0.5);
    } else if (material_id == 13) {
        color = mix(color, texture(u_texture_13, uv_0).rgb, 0.5);
    }else if (material_id == 14) {
        color = mix(color, texture(u_texture_14, uv_0).rgb, 0.5);
    }else if (material_id == 15) {
        color = mix(color, texture(u_texture_15, uv_0).rgb, 0.5);
    }else if (material_id == 16) {
        color = mix(color, texture(u_texture_16, uv_0).rgb, 0.5);
    }else if (material_id == 17) {
        color = mix(color, texture(u_texture_17, uv_0).rgb, 0.5);
    }else if (material_id == 18) {
        color = mix(color, texture(u_texture_18, uv_0).rgb, 0.5);
    }else if (material_id == 19) {
        color = mix(color, texture(u_texture_19, uv_0).rgb, 0.5);
    }else if (material_id == 20) {
        color = mix(color, texture(u_texture_20, uv_0).rgb, 0.5);
    }else if (material_id == 21) {
        color = mix(color, texture(u_texture_21, uv_0).rgb, 0.5);
    }else if (material_id == 22) {
        color = mix(color, texture(u_texture_22, uv_0).rgb, 0.5);
    }

    // Apply gamma correction
    color = pow(color, vec3(gamma));
    color = getLight(color);
    color = pow(color, vec3(1.0 / gamma));

    fragColor = vec4(color, 1.0);
}