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
                # position
                pos = self.model.vertices[face[i][0] - 1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])

                # normal
                norm = self.model.normals[face[i][2] - 1]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])

                # texCoord
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])

        self.vertBuffer = array(buffer, dtype = float32)

        self.VBO = glGenBuffers(1) # Buffer de Vertices
        self.VAO = glGenVertexArrays(1) # Array de Vértices

    def renderInScene(self):
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)

        # Los vertices
        glBufferData(GL_ARRAY_BUFFER,           # ID del buffer
                     self.vertBuffer.nbytes,    # Tamaño del buffer en bytes
                     self.vertBuffer,           # Data del buffer
                     GL_STATIC_DRAW )           # Uso

        # Atributo de posicion
        glVertexAttribPointer(0,                    # Número de atributos
                              3,                    # Tamaño
                              GL_FLOAT,             # Tipo
                              GL_FALSE,             # Esta normalizado o no
                              4 * 8,                # Paso
                              ctypes.c_void_p(0))   # Offset

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
        glTexImage2D(GL_TEXTURE_2D,                     # Tipo de textura
                     0,                                 # Nivel
                     GL_RGB,                            # Formato
                     self.textureSurface.get_width(),   # Ancho
                     self.textureSurface.get_height(),  # Alto
                     0,                                 # Borde
                     GL_RGB,                            # Formato
                     GL_UNSIGNED_BYTE,                  # Tipo
                     self.textureData)                  # Data

        glGenerateMipmap(GL_TEXTURE_2D)

        # Dibujar
        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3 ) # Dibujar vertices en orden   

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.scene = []

        self.pointLight = glm.vec3(-10, 0, -5)

        self.time = 0
        self.valor = 0
        self.normals = 0

        self.activeModel = None

        # View Matrix
        self.camPosition = glm.vec3(0,0,0)
        self.camRotation = glm.vec3(0,0,0) # Pitch, Yaw y Roll

        self.viewMatrix = self.getViewMatrix()

        # Projection Matrix
        self.projectionMatrix = glm.perspective(glm.radians(60),            # FOV en radianes
                                                self.width / self.height,   # Aspect Ratio
                                                0.1,                        # Distancia Near Plane
                                                1000)                       # Distancia Far plane


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

    def changeActiveModel(self):
        if len(self.scene) > 0:
            if self.activeModel in self.scene:
                currentPos = self.scene.index(self.activeModel)
            else: 
                currentPos = 0
            
            # Ultimo elemento del array
            if currentPos == (len(self.scene)-1):
                # Vuelve a empezar y si solo hay uno se queda en el mismo
                self.activeModel = self.scene[0]
            else:
                # Se cambia al siguiente modelo
                self.activeModel = self.scene[currentPos + 1]

    def update(self):
        target = glm.vec3(0,0,-5)
        self.viewMatrix = glm.lookAt(self.camPosition, target, glm.vec3(0.0, 1.0, 0.0))

    def render(self):
        glClearColor(0.2,0.2,0.2,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.active_shader)

        if self.active_shader:
            
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.viewMatrix))

            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.active_shader, "tiempo"), self.time)
            glUniform1f(glGetUniformLocation(self.active_shader, "valor"), self.valor)

            glUniform3f(glGetUniformLocation(self.active_shader, "pointLight"),
                        self.pointLight.x, self.pointLight.y, self.pointLight.z)


        if self.activeModel:
            if self.active_shader:
                glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                                   1, GL_FALSE, glm.value_ptr(self.activeModel.getModelMatrix()))
            self.activeModel.renderInScene()
        else:
            for model in self.scene:
                if self.active_shader:
                    glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                                    1, GL_FALSE, glm.value_ptr(model.getModelMatrix()))

                model.renderInScene()