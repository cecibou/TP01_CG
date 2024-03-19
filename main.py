import tkinter as tk
import math
from tkinter import messagebox

class TP_01_CG:
    
    # Função inicial para declarações de variaveis e botões
    def __init__(self, master):
        self.master = master
        self.master.title("Computação Gráfica - Trabalho prático 1")
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.points = [] # salvar pontos clicados na tela
        
        self.axes_visible = True  # Inicializa a visibilidade dos eixos aqui
        # Adiciona o fundo quadriculado
        self.draw_grid()
        
        # Entrada de texto para inserir coordenadas ou comandos de transformação
        self.entry = tk.Entry(self.master)
        self.entry.pack(side=tk.TOP)
        self.entry.bind("<Return>", self.apply_transformation) # Assumindo que você quer aplicar a transformação com Enter
        self.entry.focus_set()  # Coloca o foco na entrada de texto imediatamente

        # Botao para aplicar a transformacao
        self.button_apply_transformation = tk.Button(self.master, text="Aplicar Transformação", command=self.apply_transformation)
        self.button_apply_transformation.pack(side=tk.TOP)

        # Botão para desenhar poligono
        self.button_draw_poligon = tk.Button(self.master, text="Desenhar poligono", command=self.draw_polygon)
        self.button_draw_poligon.pack(side=tk.TOP)

        # Botão para desenhar linhas
        self.button_draw_line = tk.Button(self.master, text="Desenhar reta", command=self.draw_line)
        self.button_draw_line.pack(side=tk.TOP)

        # Botão para desenhar circuferencia
        self.button_draw_circle = tk.Button(self.master, text="Desenhar Círculo", command=self.draw_circle)
        self.button_draw_circle.pack(side=tk.TOP)
        
        # Botões para recorte
        self.button_clipping_c = tk.Button(self.master, text="Recorte Cohen-Sutherland", command=self.clipping_c)
        self.button_clipping_c.pack(side=tk.TOP)
        
        self.button_clipping_l = tk.Button(self.master, text="Recorte Liang-Barsky", command=self.clipping_l)
        self.button_clipping_l.pack(side=tk.TOP)
        
        self.button_clipping_s = tk.Button(self.master, text="Recorte Sutherland_Hodgeman", command=self.clipping_s)
        self.button_clipping_s.pack(side=tk.TOP)
        
        # Botão para limpar a tela e recomeçar o desenho
        self.button_clear_screen = tk.Button(self.master, text="Limpar Tela e Recomeçar", command=self.clear_screen)
        self.button_clear_screen.pack(side=tk.TOP)        
    
#--------------------FUNÇÕES HAVER COM A GRID----------------------------------#      
    # Função para limpar tela
    def clear_screen(self):
        self.canvas.delete("all")
        self.draw_grid()
        self.points = []
        messagebox.showinfo("Sucesso", "A tela foi limpa.")

    # Função para clicar o ponto na tela 
    def on_click(self, event):
        x = event.x
        y = event.y
        self.points.append((x, y))
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="black")

    # Função para desenhar fundo quadriculado
    def draw_grid(self):
        # Ajusta para desenhar com o ponto (0,0) no centro
        center_x, center_y = 200, 200  # Ajuste conforme o tamanho do seu canvas
        for i in range(0, 400, 20):  # Ajuste a escala conforme necessário
            self.canvas.create_line(i, 0, i, 400, fill="lightgray")
            # self.bres_gen(i, 0, i, 400, color="lightgray")
            self.canvas.create_line(0, i, 400, i, fill="lightgray")
            # self.bres_gen(0, i, 400, i, color="lightgray")
            
        # Desenha os eixos X e Y
        self.draw_axes()
    
    # Função para desenhar eixos x e y
    def draw_axes(self):
        # Verifica o estado atual dos eixos e os desenha se estiverem ativados
        if self.axes_visible:
            # self.canvas.create_line(200, 0, 200, 400, fill="black")  # Eixo Y
            self.bres_gen(200, 0, 200, 400, color="black")
            #self.canvas.create_line(0, 200, 400, 200, fill="black")  # Eixo X
            self.bres_gen(0, 200, 400, 200, color="black")
        

#--------------------FUNÇÕES PARA DESENHO POLÍGONO----------------------------------#  

    def calculate_centroid(self, points):
      x_sum = 0
      y_sum = 0
      for point in points:
          x_sum += point[0]
          y_sum += point[1]
      return x_sum / len(points), y_sum / len(points)

    def sort_points_by_angle(self, points, centroid):
      def polar_angle(point):
          return math.atan2(point[1] - centroid[1], point[0] - centroid[0])
      return sorted(points, key=polar_angle)

    def draw_polygon(self, color="black"): 
      if len(self.points) < 2:
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        self.bren(x1, y1, x2, y2, color=color)
      
      else: 
        # Certifique-se de que os pontos estão ordenados, se necessário
        centroid = self.calculate_centroid(self.points)
        sorted_points = self.sort_points_by_angle(self.points, centroid)

        # Desenha linhas entre os pontos para formar o contorno do polígono com a cor especificada
        for i in range(len(sorted_points)):
            start_point = sorted_points[i]
            end_point = sorted_points[(i + 1) % len(sorted_points)]  # Loop para o primeiro ponto após o último
            self.canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1], fill=color)
   
   
#--------------------FUNÇÕES PARA DESENHO DE RETAS----------------------------------#  
                 
    def draw_line(self):
        # Janela de seleção do algoritmo de desenho de linha
        self.draw_line_window = tk.Toplevel(self.master)
        self.draw_line_window.title("Selecionar Algoritmo de Desenho")

        # Botões para selecionar o algoritmo de desenho de linha
        self.button_dda = tk.Button(self.draw_line_window, text="DDA", command=self.draw_line_DDA)
        self.button_dda.pack(side=tk.TOP)

        self.button_bresenham = tk.Button(self.draw_line_window, text="Bresenham", command=self.draw_line_Bresenham)
        self.button_bresenham.pack(side=tk.TOP)

    def draw_line_DDA(self, color="black"):
        self.draw_line_window.destroy()
        
        if len(self.points) >= 2:
          x1, y1 = self.points[-1]
          x2, y2 = self.points[-2]
          dx = x2 - x1
          dy = y2 - y1

          if abs(dx) > abs(dy):
              steps = abs(dx)
          else:
              steps = abs(dy)

          x_incr = dx / steps
          y_incr = dy / steps
          x = x1
          y = y1

          # a função create_retangle() que colore o pixel do canvas
          self.canvas.create_rectangle(round(x), round(y), round(x)+1, round(y)+1, fill=color)

          for k in range(1, steps):
              x += x_incr
              y += y_incr
              self.canvas.create_rectangle(round(x), round(y), round(x)+1, round(y)+1, fill=color)
        else: messagebox.showinfo("Atenção", "Selecione dois pontos.")

    def draw_line_Bresenham(self):
        self.draw_line_window.destroy()
        if len(self.points) >= 2:
          x1, y1 = self.points[-1]
          x2, y2 = self.points[-2]
          self.bres_gen(x1, y1, x2, y2,color="red")
          self.canvas.update()
        else:  messagebox.showinfo("Atenção", "Selecione pelo menos dois pontos.")

    def bres_gen(self, x1, y1, x2, y2, color="black"):
        dx = x2 - x1
        dy = y2 - y1
        
        if dx >= 0:
            incrx = 1
        else:
            incrx = -1
            dx = -dx

        if dy >= 0:
            incry = 1
        else:
            incry = -1
            dy = -dy

        x = x1
        y = y1
        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy - dx)
            for i in range(dx):
                x += incrx
                if p < 0:
                    p += const1
                else:
                    y += incry
                    p += const2
                self.canvas.create_rectangle(x, y, x+1, y+1, fill=color)
                self.canvas.update()
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx - dy)
            for i in range(dy):
                y += incry
                if p < 0:
                    p += const1
                else:
                    x += incrx
                    p += const2
                self.canvas.create_rectangle(x, y, x+1, y+1, fill=color)
                self.canvas.update()

#--------------------FUNÇÕES PARA DESENHO CIRCUFERÊNCIA----------------------------------#  

    def plot_circle_points(self, xc, yc, x, y):
      self.set_pixel(xc + x, yc + y)
      self.set_pixel(xc - x, yc + y)
      self.set_pixel(xc + x, yc - y)
      self.set_pixel(xc - x, yc - y)
      self.set_pixel(xc + y, yc + x)
      self.set_pixel(xc - y, yc + x)
      self.set_pixel(xc + y, yc - x)
      self.set_pixel(xc - y, yc - x)

    def circBresenhams(self, xc, yc, r):
      x = 0
      y = r
      p = 3 - 2 * r
      while x < y:
          if p < 0:
              p += 4 * x + 6
          else:
              p += 4 * (x - y) + 10
              y -= 1
          x += 1
          self.plot_circle_points(xc, yc, x, y)

    def draw_circle(self):
        if len(self.points) >= 2:
          xc, yc = self.points[-1]
          x, y = self.points[-2]
          r = ((x - xc) ** 2 + (y - yc) ** 2) ** 0.5
          self.circBresenhams(xc, yc, int(r))
        else:  
            messagebox.showinfo("Atenção", "Selecione pelo menos dois pontos. Uso: 1° ponto: centro; 2° ponto: raio")

    def set_pixel(self, x, y):
      self.canvas.create_oval(x, y, x+1, y+1, fill="black")


#--------------------FUNÇÕES PARA TRANSFORMAÇÃO----------------------------------#  

    def translate(self, dx, dy):
      self.points = [(x + dx, y + dy) for (x, y) in self.points]
      self.redraw()

    def rotate(self, angle, pivot=None):
      if pivot is None:
          pivot = self.calculate_centroid(self.points)
      angle_rad = math.radians(angle)
      cos_angle = math.cos(angle_rad)
      sin_angle = math.sin(angle_rad)
      self.points = [((cos_angle * (x - pivot[0]) - sin_angle * (y - pivot[1])) + pivot[0],
                      (sin_angle * (x - pivot[0]) + cos_angle * (y - pivot[1])) + pivot[1])
                     for (x, y) in self.points]
      self.redraw()
  
    def scale(self, sx, sy, center=None):
      if center is None:
          center = self.calculate_centroid(self.points)
      self.points = [((x - center[0]) * sx + center[0], (y - center[1]) * sy + center[1]) for (x, y) in self.points]
      self.redraw()

    def reflect_x(self):
        self.points = [(x, 400 - y) for (x, y) in self.points]  # 400 é a altura do canvas
        self.redraw()

    def reflect_y(self):
        self.points = [(400 - x, y) for (x, y) in self.points]  # 400 é a largura do canvas
        self.redraw()

    def reflect_xy(self):
        self.points = [(400 - x, 400 - y) for (x, y) in self.points]  # 400 é a largura e altura do canvas
        self.redraw()

    def redraw(self):
      #self.canvas.delete("all")  # Limpa o canvas
      self.draw_grid()
      if len(self.points) == 1:
          for x, y in self.points:
            self.draw_point(x, y)
      elif len(self.points) == 2: 
        self.canvas.create_line(self.points[0], self.points[1], fill="red")
        for x, y in self.points:
            self.draw_point(x, y)
      elif len(self.points) > 2: 
        self.draw_polygon(color = "red")
        # Redesenhar os pontos
        for x, y in self.points:
            self.draw_point(x, y)
        
    def draw_point(self, x, y):
        radius = 2  # Define o tamanho do ponto
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline= "red", fill="red")

    def apply_transformation(self):
      input_text = self.entry.get().strip().upper()  # Captura e prepara a entrada do usuário
      parts = input_text.split()  # Separa o comando dos parâmetros

      if not parts:
          messagebox.showerror("Erro", "Entrada inválida.")
          self.entry.focus_set()
          return

      command = parts[0]  # O tipo de transformação é o primeiro elemento

      try:
          if command == "T" and len(parts) == 3:  # Translação
              dx = float(parts[1])
              dy = float(parts[2])
              self.translate(dx, dy)
          elif command == "R" and len(parts) == 2:  # Rotação
              angle = float(parts[1])
              self.rotate(angle)
          elif command == "S" and len(parts) == 3:  # Escala
              sx = float(parts[1])
              sy = float(parts[2])
              self.scale(sx, sy)
          elif command == "RX":  # Reflexão em torno do eixo X
            self.reflect_x()
          elif command == "RY":  # Reflexão em torno do eixo Y
            self.reflect_y()
          elif command == "RXY":  # Reflexão em torno de ambos os eixos
            self.reflect_xy()
          else:
              messagebox.showerror("Erro", "Comando desconhecido ou parâmetros insuficientes. Uso: T tx ty; R angulo; S sx sy; RX; RY; RXY")
      except ValueError as e:
          messagebox.showerror("Erro", f"Erro ao processar os parâmetros: {e}. Tente de novo.")

      self.entry.delete(0, tk.END)  # Limpa a entrada
      self.entry.focus_set()  # Mantém o foco na entrada de texto
    
    
#--------------------FUNÇÕES PARA RECORTE RETAS----------------------------------#    
    
    # Constantes para os códigos de região
    INSIDE = 0  # 0000
    LEFT = 1    # 0001
    RIGHT = 2   # 0010
    BOTTOM = 4  # 0100
    TOP = 8     # 1000
    
    # Função para calcular o código de região de um ponto
    def compute_code(self, x, y, xmin, ymin, xmax, ymax):
        code = self.INSIDE
        if x < xmin:
            code |= self.LEFT
        elif x > xmax:
            code |= self.RIGHT
        if y < ymin:
            code |= self.BOTTOM
        elif y > ymax:
            code |= self.TOP
        return code

    # Algoritmo de Cohen-Sutherland para clipping de linhas
    def cohen_sutherland_clip(self, x1, y1, x2, y2, xmin, ymin, xmax, ymax):
        code1 = self.compute_code(x1, y1, xmin, ymin, xmax, ymax)
        code2 = self.compute_code(x2, y2, xmin, ymin, xmax, ymax)
        aceite = False

        while True:
            if code1 == 0 and code2 == 0:
                aceite = True
                break
            elif (code1 & code2) != 0:
                break
            else:
                x, y = 1.0, 1.0
                if code1:
                    code_out = code1
                else:
                    code_out = code2

                if code_out & self.TOP:
                    x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                    y = ymax
                elif code_out & self.BOTTOM:
                    x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                    y = ymin
                elif code_out & self.RIGHT:
                    y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                    x = xmax
                elif code_out & self.LEFT:
                    y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                    x = xmin

                if code_out == code1:
                    x1, y1 = x, y
                    code1 = self.compute_code(x1, y1, xmin, ymin, xmax, ymax)
                else:
                    x2, y2 = x, y
                    code2 = self.compute_code(x2, y2, xmin, ymin, xmax, ymax)

        if aceite:
            return round(x1), round(y1), round(x2), round(y2)
        else:
            return None

    def clip_test(self, p, q, u1, u2):
        result = True
        new_u1, new_u2 = u1, u2  # Inicializamos novas variáveis para manter os possíveis novos valores de u1 e u2
        if p < 0.0:
            r = q / p
            if r > new_u2:
                result = False
            elif r > new_u1:
                new_u1 = r
        elif p > 0.0:
            r = q / p
            if r < new_u1:
                result = False
            elif r < new_u2:
                new_u2 = r
        elif q < 0.0:
            result = False
        return result, new_u1, new_u2  # Retornamos os valores atualizados junto com o resultado

    def liang_barsky(self, xmin, xmax, ymin, ymax, x1, y1, x2, y2):
        u1, u2 = 0.0, 1.0
        dx = x2 - x1
        dy = y2 - y1

        success, u1, u2 = self.clip_test(-dx, x1 - xmin, u1, u2)  # Atualizamos u1 e u2
        if success:
            success, u1, u2 = self.clip_test(dx, xmax - x1, u1, u2)
        if success:
            success, u1, u2 = self.clip_test(-dy, y1 - ymin, u1, u2)
        if success:
            success, u1, u2 = self.clip_test(dy, ymax - y1, u1, u2)
        
        if success:
            if u2 < 1.0:
                x2 = x1 + u2 * dx
                y2 = y1 + u2 * dy
            if u1 > 0.0:
                x1 = x1 + u1 * dx
                y1 = y1 + u1 * dy
        
        return round(x1), round(y1), round(x2), round(y2)

    def clipping_c(self):
        if len(self.points) <= 3:
            messagebox.showerror('Erro', 'Desenhe a janela de recorte e pelo menos uma linha para aplicar o clipping.\n\nUSO: desenhe quantas linhas preferir e por último selecione dois pontos sendo eles na diagonal.')
            return

        # Pegue os últimos dois pontos
        p1 = self.points[-2]
        p2 = self.points[-1]

        # Calcule os pontos refletidos para formar um retângulo com angulos 90°
        p3 = (p1[0], p2[1])
        p4 = (p2[0], p1[1])

        # Defina a janela de recorte com esses quatro pontos
        xmin = min(p1[0], p2[0])
        ymin = min(p1[1], p2[1])
        xmax = max(p1[0], p2[0])
        ymax = max(p1[1], p2[1])

        # Atualize a lista de pontos, removendo os dois últimos e adicionando os quatro da janela de recorte
        self.points = self.points[:-2] + [p1, p3, p2, p4]

        # Aplica o algoritmo de recorte Cohen-Sutherland usando a nova janela de recorte
        new_points = []
        for i in range(0, len(self.points)-4, 2):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            clipped_line = self.cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax)
            if clipped_line:
                new_points.extend(clipped_line)

        clipping_area = [p1, p3, p2, p4]
        # Limpa o canvas e redesenha
        self.canvas.delete("all")
        self.draw_grid()
        # Desenha a nova janela de recorte
        self.canvas.create_polygon(clipping_area, outline='blue', fill='', dash=(3, 5), width=2)
        # Desenha as linhas recortadas
        for i in range(0, len(new_points)-1, 4):
            self.canvas.create_line(new_points[i], new_points[i+1], new_points[i+2], new_points[i+3], fill="red")

    def clipping_l(self):
        if len(self.points) <= 3:
            messagebox.showerror('Erro', 'Desenhe pelo menos dois pontos para formar a janela de recorte.\n\nUSO: desenhe quantas linhas preferir e por último selecione dois pontos sendo eles na diagonal.')
            return

        # Pegue os últimos dois pontos
        p1 = self.points[-2]
        p2 = self.points[-1]

        # Calcule os pontos refletidos para formar um retângulo com angulos 90°
        p3 = (p1[0], p2[1])
        p4 = (p2[0], p1[1])

        # Defina a janela de recorte com esses quatro pontos
        xmin = min(p1[0], p2[0])
        ymin = min(p1[1], p2[1])
        xmax = max(p1[0], p2[0])
        ymax = max(p1[1], p2[1])

        # Atualize a lista de pontos, removendo os dois últimos e adicionando os quatro da janela de recorte
        self.points = self.points[:-2] + [p1, p3, p2, p4]

        # Aplica o algoritmo de recorte Liang-Barsky usando a nova janela de recorte
        new_points = []
        for i in range(0, len(self.points)-4, 2):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            clipped_line = self.liang_barsky(xmin, xmax, ymin, ymax, x1, y1, x2, y2)
            if clipped_line:
                new_points.extend(clipped_line)

        clipping_area = [p1, p3, p2, p4]
        # Limpa o canvas e redesenha
        self.canvas.delete("all")
        self.draw_grid()
        # Desenha a nova janela de recorte
        self.canvas.create_polygon(clipping_area, outline='blue', fill='', dash=(3, 5), width=2)
        # Desenha as linhas recortadas
        for i in range(0, len(new_points)-1, 4):
            self.canvas.create_line(new_points[i], new_points[i+1], new_points[i+2], new_points[i+3], fill="red")

    
#NÃO faz parte do enunciado, mas é um incremento#
#--------------------FUNÇÕES PARA RECORTE POLÍGONO----------------------------------#

    def ponto_intersecao(self, v1, v2, borda):
        A, B = v1, v2
        # A equação da borda será necessária para calcular a interseção
        if borda == 'ymax':
            # Calcular a interseção com ymax
            x = A[0] + (B[0] - A[0]) * (self.ymax - A[1]) / (B[1] - A[1])
            return (x, self.ymax)
        elif borda == 'xmax':
            # Calcular a interseção com xmax
            y = A[1] + (B[1] - A[1]) * (self.xmax - A[0]) / (B[0] - A[0])
            return (self.xmax, y)
        elif borda == 'ymin':
            # Calcular a interseção com ymin
            x = A[0] + (B[0] - A[0]) * (self.ymin - A[1]) / (B[1] - A[1])
            return (x, self.ymin)
        elif borda == 'xmin':
            # Calcular a interseção com xmin
            y = A[1] + (B[1] - A[1]) * (self.xmin - A[0]) / (B[0] - A[0])
            return (self.xmin, y)

    def dentro(self, ponto, borda):
        if borda == 'ymax':
            return ponto[1] <= self.ymax
        elif borda == 'xmax':
            return ponto[0] <= self.xmax
        elif borda == 'ymin':
            return ponto[1] >= self.ymin
        elif borda == 'xmin':
            return ponto[0] >= self.xmin

    def recorta_poligono(self, vertices, bordas_recorte):
        new_vertices = vertices
        for borda in bordas_recorte:
            input_list = new_vertices
            new_vertices = []
            v1 = input_list[-1]

            for v2 in input_list:
                if self.dentro(v2, borda):
                    if not self.dentro(v1, borda):
                        new_vertices.append(self.ponto_intersecao(v1, v2, borda))
                    new_vertices.append(v2)
                elif self.dentro(v1, borda):
                    new_vertices.append(self.ponto_intersecao(v1, v2, borda))
                v1 = v2
        return new_vertices
    
    def clipping_s(self):
        if len(self.points) <= 4:
            messagebox.showerror('Erro', 'Desenhe a janela e um polígono (min 3 pontos) para aplicar o clipping.\n\nUSO: desenhe o polígono e por último selecione dois pontos sendo eles na diagonal.')
            return

        # Pegue os últimos dois pontos para a janela de recorte
        p1 = self.points[-2]
        p2 = self.points[-1]

        # Calcule os pontos refletidos para formar um retângulo
        p3 = (p1[0], p2[1])
        p4 = (p2[0], p1[1])

        # Atualize a janela de recorte com os pontos calculados
        clipping_area = [p1, p3, p2, p4]
        xmin, ymin = min(p1[0], p2[0]), min(p1[1], p2[1])
        xmax, ymax = max(p1[0], p2[0]), max(p1[1], p2[1])

        # Define as bordas da janela de recorte
        self.xmin, self.ymin, self.xmax, self.ymax = xmin, ymin, xmax, ymax

        # Os pontos do polígono são todos exceto os dois últimos
        poligono = self.points[:-2]

        # Clipping do polígono usando Sutherland-Hodgeman
        new_vertices = self.recorta_poligono(poligono, ['xmin', 'ymin', 'xmax', 'ymax'])

        # Limpa o canvas e redesenha
        self.canvas.delete("all")
        self.draw_grid()
        # Desenha a janela de recorte
        self.canvas.create_polygon(clipping_area, outline='blue', fill='', dash=(3, 5), width=2)
        # Desenha o polígono recortado
        self.points = new_vertices
        if new_vertices:
            new_vertices.append(new_vertices[0])  # Fechar o polígono
            #self.canvas.create_polygon(new_vertices, outline='red', fill='', width=2)
            self.draw_polygon(color='red')

        # Atualiza a lista de pontos com os novos vértices do polígono recortado
        self.points = new_vertices

    
#fim da classe

root = tk.Tk()
app = TP_01_CG(root)
root.mainloop()