@vertexShader

varying vec2 var_TexCoord;

void setupSurfaceData(vec4 eyeSpacePosition)
{
	var_TexCoord.x = gl_MultiTexCoord0.x;
	var_TexCoord.y = gl_MultiTexCoord0.y;
}
