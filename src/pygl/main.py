import ctypes
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLUT as glut
import sys

from shader import Shader


def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
    glut.glutSwapBuffers()

def reshape(width, height):
    gl.glViewport(0, 0, width, height)

def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit()

glut.glutInit()
glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
glut.glutCreateWindow("Hello world!")
glut.glutReshapeWindow(512, 512)
glut.glutReshapeFunc(reshape)
glut.glutDisplayFunc(display)
glut.glutKeyboardFunc(keyboard)

program = gl.glCreateProgram()
vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

# Load shader programs.
vertex_code = Shader("shaders/0_intro/shader.vert").load()
fragment_code = Shader("shaders/0_intro/shader.frag").load()

gl.glShaderSource(vertex, vertex_code)
gl.glShaderSource(fragment, fragment_code)

# Compile shader source.
gl.glCompileShader(vertex)
if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Vertex shader compilation failed.")

gl.glCompileShader(fragment)
if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
    error = gl.glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Fragment shader compilation failed.")

gl.glAttachShader(program, vertex)
gl.glAttachShader(program, fragment)

gl.glLinkProgram(program)
if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
    print(gl.glGetProgramInfoLog(program))
    raise RuntimeError("Linking failed.")

gl.glDetachShader(program, vertex)
gl.glDetachShader(program, fragment)

# Make program the default program
gl.glUseProgram(program)

# Build data.
dtype = np.dtype([('position', np.float32, 2)])
data = np.zeros(4, dtype=dtype)
data['position'] = [[-1, 1], [1, 1], [-1, -1], [1, -1]]

# Request a buffer on GPU.
buffer = gl.glGenBuffers(1)

# Activate this buffer as current.
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)

# Upload data to GPU.
gl.glBufferData(gl.GL_ARRAY_BUFFER, data.nbytes, data, gl.GL_DYNAMIC_DRAW)

# Tell GPU how to read buffer data. Our data is contiguous, so this is straigh-forward.
stride = data.strides[0]
offset = ctypes.c_void_p(0)
loc = gl.glGetAttribLocation(program, "position")
gl.glEnableVertexAttribArray(loc)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, buffer)
gl.glVertexAttribPointer(loc, 2, gl.GL_FLOAT, False, stride, offset)

# Set colour uniform.
loc = gl.glGetUniformLocation(program, "color")
gl.glUniform4f(loc, 0.0, 0.0, 1.0, 1.0)

glut.glutMainLoop()


