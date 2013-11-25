@vertexShader

varying vec2 var_TexCoord;

void setupSurfaceData(vec4 eyeSpacePosition)
{
	var_TexCoord = gl_MultiTexCoord0.xy;
}
