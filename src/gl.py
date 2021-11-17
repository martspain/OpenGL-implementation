from pygame import image
import glm
from numpy import array, float32
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import obj

class ModelObj(object):
    def __init__(self, objName, textureName):

        self.model = obj.Obj(objName)

        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

        self.textureSurface = image.load(textureName)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)


    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMatrix = glm.translate(identity, self.position)

        pitch = glm.rotate(identity, glm.radians( self.rotation.x ), glm.vec3(1,0,0) )
        yaw   = glm.rotate(identity, glm.radians( self.rotation.y ), glm.vec3(0,1,0) )
        roll  = glm.rotate(identity, glm.radians( self.rotation.z ), glm.vec3(0,0,1) )
        rotationMatrix = pitch * yaw * roll

        scaleMatrix = glm.scale(identity, self.scale)

        return translateMatrix * rotationMatrix * scaleMatrix



    def createVertexBuffer(self):

        buffer = []

        for face in self.model.faces:
            for i in range(3):
                # positions
                pos = self.model.vertices[face[i][0] - 1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])

                # normals
                norm = self.model.normals[face[i][2] - 1]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])

                # texCoords
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])

        self.vertBuffer = array(buffer, dtype = float32)

        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object

    def renderInScene(self):
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Los vertices
        glBufferData(GL_ARRAY_BUFFER,           #Buffer ID
                     self.vertBuffer.nbytes,    #Buffer size in bytes
                     self.vertBuffer,           #Buffer data
                     GL_STATIC_DRAW )           #Usage

        # Atributo de posicion
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # It it normalized?
                              4 * 8,            # Stride
                              ctypes.c_void_p(0)) # Offset

        glEnableVertexAttribArray(0)

        # Atributo de normales
        glVertexAttribPointer(1,
                              3,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4 * 3))

        glEnableVertexAttribArray(1)


        # Atributo de coordenadas de textura
        glVertexAttribPointer(2,
                              2,
                              GL_FLOAT,
                              GL_FALSE,
                              4 * 8,
                              ctypes.c_void_p(4 * 6))

        glEnableVertexAttribArray(2)

        # Dar textura
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D,                     # Texture type
                     0,                                 # Level
                     GL_RGB,                            # Format
                     self.textureSurface.get_width(),   # Width
                     self.textureSurface.get_height(),  # Height
                     0,                                 # Border
                     GL_RGB,                            # Format
                     GL_UNSIGNED_BYTE,                  # Type
                     self.textureData)                  # Data

        glGenerateMipmap(GL_TEXTURE_2D)



        # Dibujar
        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3 ) # Para dibujar vertices en orden

class Prop(object):
    def __init__(self, verts, indices):

        self.createVertexBuffer(verts, indices)

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)
    
    def getModelMatrix(self):
        identity = glm.mat4(1)

        translateMatrix = glm.translate(identity, self.position)
        pitch = glm.rotate(identity, glm.radians( self.rotation.x ), glm.vec3(1,0,0) )
        yaw   = glm.rotate(identity, glm.radians( self.rotation.y ), glm.vec3(0,1,0) )
        roll  = glm.rotate(identity, glm.radians( self.rotation.z ), glm.vec3(0,0,1) )
        rotationMatrix = pitch * yaw * roll
        scaleMatrix = glm.scale(identity, self.scale)
        return translateMatrix * rotationMatrix * scaleMatrix

    def createVertexBuffer(self, verts, indices):
        self.vertBuffer = verts
        self.indexBuffer = indices


        self.VBO = glGenBuffers(1) #Vertex Buffer Object
        self.VAO = glGenVertexArrays(1) #Vertex Array Object
        self.EAO = glGenBuffers(1) #Element Array Object

    def renderInScene(self):

        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EAO)

        glBufferData(GL_ARRAY_BUFFER,           #Buffer ID
                     self.vertBuffer.nbytes,    #Buffer size in bytes
                     self.vertBuffer,           #Buffer data
                     GL_STATIC_DRAW )           #Usage

        glBufferData(GL_ELEMENT_ARRAY_BUFFER,   #Buffer ID
                     self.indexBuffer.nbytes,    #Buffer size in bytes
                     self.indexBuffer,           #Buffer data
                     GL_STATIC_DRAW )           #Usage

        # Atributo de posicion
        glVertexAttribPointer(0,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # It it normalized?
                              4 * 6,            # Stride
                              ctypes.c_void_p(0)) # Offset

        glEnableVertexAttribArray(0)

        # Atributo de color
        glVertexAttribPointer(1,                # Attribute number
                              3,                # Size
                              GL_FLOAT,         # Type
                              GL_FALSE,         # It it normalized?
                              4 * 6,            # Stride
                              ctypes.c_void_p(4 * 3)) # Offset

        glEnableVertexAttribArray(1)



        #glDrawArrays(GL_TRIANGLES, 0, 3 ) # Para dibujar vertices en orden
        glDrawElements(GL_TRIANGLES, len(self.indexBuffer), GL_UNSIGNED_INT, None) #Para dibujar con indices
    

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []

        self.pointLight = glm.vec3(-10, 0, -5)

        self.tiempo = 0
        self.valor = 0

        # View Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0) # pitch, yaw, roll

        # Projection Matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),            # FOV en radianes
                                                self.width / self.height,   # Aspect Ratio
                                                0.1,                        # Near Plane distance
                                                1000)                       # Far plane distance


    def getViewMatrix(self):
        identity = glm.mat4(1)

        translateMatrix = glm.translate(identity, self.camPosition)

        pitch = glm.rotate(identity, glm.radians( self.camRotation.x ), glm.vec3(1,0,0) )
        yaw   = glm.rotate(identity, glm.radians( self.camRotation.y ), glm.vec3(0,1,0) )
        roll  = glm.rotate(identity, glm.radians( self.camRotation.z ), glm.vec3(0,0,1) )

        rotationMatrix = pitch * yaw * roll

        camMatrix = translateMatrix * rotationMatrix

        return glm.inverse(camMatrix)


    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None and fragShader is not None:
            self.active_shader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                 compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None


    def render(self):
        glClearColor(0.2,0.2,0.2,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.active_shader)

        if self.active_shader:
            
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.getViewMatrix()))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.active_shader, "tiempo"), self.tiempo)
            glUniform1f(glGetUniformLocation(self.active_shader, "valor"), self.valor)

            glUniform3f(glGetUniformLocation(self.active_shader, "pointLight"),
                        self.pointLight.x, self.pointLight.y, self.pointLight.z)


        for model in self.scene:
            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                                   1, GL_FALSE, glm.value_ptr(model.getModelMatrix()))

            model.renderInScene()