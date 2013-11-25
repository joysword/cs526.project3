@vertexShader

varying vec2 var_TexCoord;

void setupSurfaceData(vec4 eyeSpacePosition)
{
	var_TexCoord.x = gl_MultiTexCoord0.x+132;
	var_TexCoord.y = gl_MultiTexCoord0.x+62;
}
